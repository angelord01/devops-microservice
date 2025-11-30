import pytest
import requests
import json
from src.app import app
from src.auth_manager import api_manager

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_complete_integration_flow(client):
    """Test de integración completo del flujo DevOps"""
    
    # 1. Generar un JWT único para la transacción
    jwt_payload = {
        "transaction_id": "test-integration-001",
        "purpose": "devops-assessment"
    }
    jwt_token = api_manager.generate_jwt(jwt_payload)
    
    # 2. Preparar headers con API Key y JWT
    headers = {
        'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
        'X-JWT-KWY': jwt_token,
        'Content-Type': 'application/json'
    }
    
    # 3. Datos del payload según especificación
    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeTol.ffeSec": 45
    }
    
    # 4. Ejecutar la petición al endpoint /DevOps
    response = client.post('/DevOps', json=payload, headers=headers)
    
    # 5. Verificar respuesta exitosa
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert "message" in response_data
    assert "Juan Perez" in response_data["message"]
    assert "your message will be send" in response_data["message"]
    
    # 6. Verificar que el JWT fue marcado como usado
    stats = api_manager.get_transaction_stats()
    assert stats["used_tokens"] >= 1

def test_health_endpoint_integration(client):
    """Test del endpoint de salud con estadísticas"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data["status"] == "healthy"
    assert data["service"] == "devops-microservice"
    assert "transaction_stats" in data
    assert "total_transactions" in data["transaction_stats"]

def test_jwt_generation_endpoint(client):
    """Test del endpoint de generación de JWT"""
    test_payload = {"test": "integration", "user": "ci-cd-pipeline"}
    response = client.post('/admin/generate-jwt', json=test_payload)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "jwt_token" in data
    
    # Verificar que el token es válido
    try:
        api_manager.validate_jwt(data["jwt_token"])
        assert True
    except Exception:
        assert False, "Generated JWT should be valid"

def test_error_scenarios_integration(client):
    """Test de escenarios de error en integración"""
    
    # Test sin API Key
    response = client.post('/DevOps', json={})
    assert response.status_code == 401
    
    # Test con API Key incorrecta
    headers = {
        'X-Parse-REST-API-Key': 'wrong-key',
        'Content-Type': 'application/json'
    }
    response = client.post('/DevOps', json={}, headers=headers)
    assert response.status_code == 401
    
    # Test con método incorrecto
    response = client.get('/DevOps')
    assert response.status_code == 405
    assert b"ERROR" in response.data

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
