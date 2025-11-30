from flask import Flask, request, jsonify
import os
import logging
from .auth_manager import api_manager  # Importación relativa corregida

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/DevOps", methods=["POST"])
def devops_endpoint():
    """
    Endpoint principal que requiere:
    - API Key en headers: X-Parse-REST-API-Key
    - JWT en headers: X-JWT-KWY
    - JSON payload específico
    """
    try:
        # Validar API Key
        api_key = request.headers.get("X-Parse-REST-API-Key")
        if not api_key or not api_manager.validate_api_key(api_key):
            logger.warning("Intento de acceso con API Key inválida")
            return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

        # Validar JWT
        jwt_token = request.headers.get("X-JWT-KWY")
        if not jwt_token:
            return jsonify({"error": "JWT token required"}), 401

        try:
            jwt_payload = api_manager.validate_jwt(jwt_token)
            logger.info(
                f"JWT válido procesado para transacción: {jwt_payload.get('jti')}"
            )
        except Exception as e:
            return jsonify({"error": f"JWT validation failed: {str(e)}"}), 401

        # Validar que es JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()

        # Validar campos requeridos en el payload
        required_fields = ["message", "to", "from", "timeTol.ffeSec"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return (
                jsonify(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"}
                ),
                400,
            )

        # Validar tipos de datos
        if not isinstance(data.get("timeTol.ffeSec"), int):
            return jsonify({"error": "timeTol.ffeSec must be an integer"}), 400

        # Crear respuesta exitosa
        response_message = f"Hello {data['to']} your message will be send"

        logger.info(f"Mensaje procesado exitosamente para: {data['to']}")

        return jsonify({"message": response_message}), 200

    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/DevOps", methods=["GET", "PUT", "DELETE", "PATCH", "OPTIONS"])
def other_methods():
    """Maneja todos los otros métodos HTTP retornando ERROR"""
    logger.warning(f"Método no permitido: {request.method}")
    return "ERROR", 405


@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint para verificar salud del servicio"""
    stats = api_manager.get_transaction_stats()
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "devops-microservice",
                "transaction_stats": stats,
            }
        ),
        200,
    )


@app.route("/admin/generate-jwt", methods=["POST"])
def generate_jwt():
    """Endpoint para generar JWT tokens (solo para testing)"""
    try:
        data = request.get_json() or {}
        token = api_manager.generate_jwt(data)
        return jsonify({"jwt_token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
