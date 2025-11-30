"""
Módulo para gestión de API Keys y validación JWT
"""

import os
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt


class APIManager:
    def __init__(self):
        # API Key requerida por el ejercicio
        self.required_api_key = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"

        # En producción, esto vendría de variables de entorno o secret manager
        self.jwt_secret = os.getenv("JWT_SECRET", "devops-assessment-secret-key")
        self.jwt_algorithm = "HS256"

        # Registro de transacciones (en producción usaríamos una base de datos)
        self.transactions = {}
        self.used_tokens = set()  # Conjunto para tokens usados

    def validate_api_key(self, api_key: str) -> bool:
        """Valida que la API Key sea correcta"""
        return api_key == self.required_api_key

    def generate_jwt(self, payload: Dict[str, Any]) -> str:
        """Genera un JWT único para la transacción"""
        # Asegurar que cada JWT sea único
        unique_payload = payload.copy()
        unique_payload["jti"] = str(uuid.uuid4())  # JWT ID único
        unique_payload["iat"] = datetime.now(timezone.utc)  # Issued at
        unique_payload["exp"] = datetime.now(timezone.utc) + timedelta(
            minutes=10
        )  # Expira en 10 min

        token = jwt.encode(
            unique_payload, self.jwt_secret, algorithm=self.jwt_algorithm
        )

        # Registrar la transacción
        self.transactions[unique_payload["jti"]] = {
            "generated_at": unique_payload["iat"].isoformat(),
            "expires_at": unique_payload["exp"].isoformat(),
            "payload": payload,
            "used": False,
        }

        return token

    def validate_jwt(self, token: str) -> Dict[str, Any]:
        """Valida un JWT token y retorna el payload si es válido"""
        try:
            payload = jwt.decode(
                token, self.jwt_secret, algorithms=[self.jwt_algorithm]
            )

            # Verificar que el token no haya sido usado antes
            if token in self.used_tokens:
                raise jwt.InvalidTokenError("JWT token has already been used")

            # Verificar que el JWT ID existe en las transacciones
            jti = payload.get("jti")
            if jti not in self.transactions:
                raise jwt.InvalidTokenError("JWT token not found in transactions")

            # Marcar como usado
            self.used_tokens.add(token)
            self.transactions[jti]["used"] = True
            self.transactions[jti]["used_at"] = datetime.now(timezone.utc).isoformat()

            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("JWT token has expired")
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid JWT token: {str(e)}")

    def get_transaction_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de las transacciones"""
        total = len(self.transactions)
        used = len([t for t in self.transactions.values() if t.get("used")])
        active = total - used

        return {
            "total_transactions": total,
            "active_tokens": active,
            "used_tokens": used,
        }


# Instancia global del API Manager
api_manager = APIManager()
