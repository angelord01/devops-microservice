import pytest
import json
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_devops_endpoint_success(client):
    """Test para el endpoint /DevOps con datos válidos"""
    # Primero necesitamos generar un JWT válido
    from src.auth_manager import api_manager

    jwt_token = api_manager.generate_jwt({"test": "devops"})

    headers = {
        "X-Parse-REST-API-Key": "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c",
        "X-JWT-KWY": jwt_token,
        "Content-Type": "application/json",
    }

    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeTol.ffeSec": 45,
    }

    response = client.post("/DevOps", json=data, headers=headers)

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert "message" in response_data
    assert "Juan Perez" in response_data["message"]


def test_devops_endpoint_missing_api_key(client):
    """Test sin API Key debe fallar"""
    headers = {"Content-Type": "application/json"}

    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeTol.ffeSec": 45,
    }

    response = client.post("/DevOps", json=data, headers=headers)
    assert response.status_code == 401


def test_devops_endpoint_wrong_api_key(client):
    """Test con API Key incorrecta"""
    headers = {
        "X-Parse-REST-API-Key": "wrong-api-key",
        "Content-Type": "application/json",
    }

    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeTol.ffeSec": 45,
    }

    response = client.post("/DevOps", json=data, headers=headers)
    assert response.status_code == 401


def test_devops_endpoint_missing_jwt(client):
    """Test sin JWT debe fallar"""
    headers = {
        "X-Parse-REST-API-Key": "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c",
        "Content-Type": "application/json",
    }

    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeTol.ffeSec": 45,
    }

    response = client.post("/DevOps", json=data, headers=headers)
    assert response.status_code == 401


def test_devops_endpoint_missing_fields(client):
    """Test con campos faltantes en el payload"""
    from src.auth_manager import api_manager

    jwt_token = api_manager.generate_jwt({"test": "missing_fields"})

    headers = {
        "X-Parse-REST-API-Key": "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c",
        "X-JWT-KWY": jwt_token,
        "Content-Type": "application/json",
    }

    # Datos incompletos (falta 'to')
    data = {"message": "This is a test", "from": "Rita Asturia", "timeTol.ffeSec": 45}

    response = client.post("/DevOps", json=data, headers=headers)
    assert response.status_code == 400


def test_other_methods_return_error(client):
    """Test que otros métodos HTTP retornan ERROR"""
    methods = ["GET", "PUT", "DELETE", "PATCH"]

    for method in methods:
        if method == "GET":
            response = client.get("/DevOps")
        elif method == "PUT":
            response = client.put("/DevOps")
        elif method == "DELETE":
            response = client.delete("/DevOps")
        elif method == "PATCH":
            response = client.patch("/DevOps")

        assert response.status_code == 405
        assert b"ERROR" in response.data


def test_health_endpoint(client):
    """Test para el endpoint de salud"""
    response = client.get("/health")
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["status"] == "healthy"
    assert response_data["service"] == "devops-microservice"
