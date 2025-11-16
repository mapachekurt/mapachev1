# Outputs for SaaS Agent Terraform module

output "endpoint_id" {
  description = "Vertex AI endpoint ID"
  value       = google_vertex_ai_endpoint.agent_endpoint.id
}

output "endpoint_name" {
  description = "Vertex AI endpoint name"
  value       = google_vertex_ai_endpoint.agent_endpoint.name
}

output "service_name" {
  description = "Cloud Run service name"
  value       = google_cloud_run_service.agent_service.name
}

output "service_url" {
  description = "Cloud Run service URL"
  value       = google_cloud_run_service.agent_service.status[0].url
}

output "service_account_email" {
  description = "Service account email address"
  value       = google_service_account.agent_sa.email
}

output "service_account_name" {
  description = "Service account name"
  value       = google_service_account.agent_sa.name
}

output "secret_id" {
  description = "Secret Manager secret ID for API key"
  value       = google_secret_manager_secret.agent_api_key.secret_id
}

output "agent_config" {
  description = "Complete agent configuration"
  value = {
    agent_id     = var.agent_id
    agent_name   = var.agent_name
    display_name = var.display_name
    tier         = var.tier
    category     = var.category
    environment  = var.environment
    endpoint_url = google_cloud_run_service.agent_service.status[0].url
  }
}
