# DevOps Microservice - Banco Pichincha Assessment

## 📋 Descripción del Proyecto

Microservicio REST desarrollado para la evaluación técnica de DevOps de Banco Pichincha. Implementa un endpoint seguro `/DevOps` con autenticación por API Key y JWT.

## 🏗️ Arquitectura
devops-microservice/
├── src/ # Código fuente del microservicio
│ ├── app.py # Aplicación Flask principal
│ └── auth_manager.py # Gestión de API Keys y JWT
├── tests/ # Tests automatizados
├── kubernetes/ # Manifiestos de Kubernetes
├── terraform/ # Infraestructura como código
├── .github/workflows/ # Pipeline CI/CD
└── Dockerfile # Containerización

## 🚀 Características

- **Endpoint REST seguro** `/DevOps` (POST only)
- **Autenticación** con API Key y JWT único por transacción
- **Containerizado** con Docker
- **Orquestación** Kubernetes con Load Balancer
- **Infrastructure as Code** con Terraform
- **CI/CD Pipeline** automático con GitHub Actions
- **Tests automatizados** con 88% de cobertura
- **Análisis estático** de código y seguridad

## 📊 Métricas de Calidad

- ✅ **19 tests** automatizados - Todos pasando
- ✅ **88% cobertura** de código
- ✅ **Análisis estático** integrado (flake8, pylint, bandit)
- ✅ **Escaneo de seguridad** con Trivy
- ✅ **Prevención de replay attacks** en JWT

## 🔐 Endpoint Principal

### `POST /DevOps`

**Headers requeridos:**
```http
X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c
X-JWT-KWY: <jwt-token-único>
Content-Type: application/json

payload json
{
  "message": "This is a test",
  "to": "Juan Perez",
  "from": "Rita Asturia",
  "timeTol.ffeSec": 45
}
respuesta exitosa
{
  "message": "Hello Juan Perez your message will be send"
}

🛠️ Instalación y Despliegue
Prerrequisitos
Docker

Kubernetes (opcional)

Python 3.9+

ejecucion local
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python -m pytest tests/ -v

# Ejecutar servidor
python src/app.py

Containerización
# Construir imagen
docker build -t devops-microservice .

# Ejecutar contenedor
docker run -p 5000:5000 devops-microservice

Kubernetes
# Aplicar manifiestos
kubectl apply -f kubernetes/

terraform
cd terraform
terraform init
terraform apply

🔄 Pipeline CI/CD
El pipeline automatizado incluye:

Análisis estático - flake8, pylint, bandit

Testing - 19 tests con cobertura 88%

Security Scan - Trivy vulnerability scanning

Build - Containerización con Docker

Deploy - Despliegue automático a staging/producción

Ramas:

main → Despliegue automático a producción

develop → Despliegue a staging

feature/* → Solo testing y build

🧪 Testing
# Ejecutar todos los tests
python -m pytest tests/ -v

# Ejecutar tests con cobertura
python -m pytest tests/ -v --cov=src --cov-report=html

# Tests específicos
python -m pytest tests/test_app.py -v
python -m pytest tests/test_auth_manager.py -v

📈 Monitoreo y Salud

Health Check
GET /health

Response
{
  "status": "healthy",
  "service": "devops-microservice",
  "transaction_stats": {
    "total_transactions": 15,
    "active_tokens": 5,
    "used_tokens": 10
  }
}

🔒 Seguridad
Validación de API Key requerida

JWT único por transacción con expiración

Prevención de replay attacks

Escaneo de vulnerabilidades en CI/CD

Análisis estático de seguridad con Bandit

👥 Responsabilidades Cumplidas
Microservicio containerizado

Load balancer con mínimo 2 nodos

Infrastructure as Code versionado

Pipeline CI/CD como código

Tests automatizados

Análisis estático de código

Crecimiento dinámico (HPA)

API Manager para API Key y JWT

Clean Code y TDD

Cobertura >80% alcanzada (88%)

🚀 URLs de Despliegue
Production: http://devops-microservice-service.production.svc.cluster.local

Staging: http://devops-microservice-service.staging.svc.cluster.local

Health Check: /health


Desarrollado por: Angel Chavez
Para: Banco Pichincha - DevOps Technical Assessment
Fecha: 30-11-2025