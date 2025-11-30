import time

import jwt
import pytest

from src.auth_manager import APIManager


@pytest.fixture
def auth_manager():
    return APIManager()


def test_validate_correct_api_key(auth_manager):
    """Test que valida una API Key correcta"""
    valid_api_key = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
    assert auth_manager.validate_api_key(valid_api_key) == True


def test_validate_incorrect_api_key(auth_manager):
    """Test que rechaza una API Key incorrecta"""
    invalid_api_key = "invalid-api-key-123"
    assert auth_manager.validate_api_key(invalid_api_key) == False


def test_generate_and_validate_jwt(auth_manager):
    """Test de generación y validación de JWT"""
    test_payload = {"user": "test", "action": "devops"}
    token = auth_manager.generate_jwt(test_payload)

    # Validar que el token se puede decodificar
    payload = auth_manager.validate_jwt(token)
    assert payload["user"] == "test"
    assert payload["action"] == "devops"
    assert "jti" in payload  # JWT ID debe estar presente


def test_jwt_uniqueness(auth_manager):
    """Test que cada JWT generado es único"""
    payload = {"test": "data"}
    token1 = auth_manager.generate_jwt(payload)
    token2 = auth_manager.generate_jwt(payload)

    assert token1 != token2  # Los tokens deben ser diferentes


def test_jwt_expiration(auth_manager):
    """Test de expiración de JWT (simulado)"""
    # Este test verifica la estructura, no la expiración real
    payload = {"test": "expiration"}
    token = auth_manager.generate_jwt(payload)

    decoded = auth_manager.validate_jwt(token)
    assert "exp" in decoded  # Campo de expiración debe estar presente


def test_transaction_stats(auth_manager):
    """Test de estadísticas de transacciones"""
    initial_stats = auth_manager.get_transaction_stats()

    # Generar algunos tokens
    for i in range(3):
        auth_manager.generate_jwt({"iteration": i})

    stats_after = auth_manager.get_transaction_stats()
    assert stats_after["total_transactions"] == initial_stats["total_transactions"] + 3
    assert stats_after["active_tokens"] == initial_stats["active_tokens"] + 3


def test_validate_used_jwt(auth_manager):
    """Test que un JWT usado no puede reutilizarse"""
    payload = {"test": "reuse"}
    token = auth_manager.generate_jwt(payload)

    # Usar el token una vez
    auth_manager.validate_jwt(token)

    # Intentar usar el mismo token otra vez - debe fallar
    with pytest.raises(jwt.InvalidTokenError, match="JWT token has already been used"):
        auth_manager.validate_jwt(token)


def test_invalid_jwt(auth_manager):
    """Test con JWT inválido"""
    with pytest.raises(jwt.InvalidTokenError):
        auth_manager.validate_jwt("invalid.jwt.token")


if __name__ == "__main__":
    pytest.main([__file__])
