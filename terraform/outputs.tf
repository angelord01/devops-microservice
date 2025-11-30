output "application_url" {
  description = "URL de acceso a la aplicación"
  value       = "http://${kubernetes_service.devops_service.status[0].load_balancer[0].ingress[0].ip}"
}

output "namespace" {
  description = "Namespace donde se desplegó la aplicación"
  value       = kubernetes_namespace.devops_assessment.metadata[0].name
}

output "deployment_name" {
  description = "Nombre del deployment de Kubernetes"
  value       = kubernetes_deployment.devops_microservice.metadata[0].name
}

output "service_name" {
  description = "Nombre del servicio Kubernetes"
  value       = kubernetes_service.devops_service.metadata[0].name
}
