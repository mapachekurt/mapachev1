# Terraform module for SaaS Agent deployment
# Google Vertex AI Agent Engine

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "agent_name" {
  description = "Name of the SaaS agent"
  type        = string
}

variable "agent_id" {
  description = "Unique agent ID"
  type        = string
}

variable "display_name" {
  description = "Display name for the agent"
  type        = string
}

variable "tier" {
  description = "Agent tier (tier_1 through tier_5)"
  type        = string
}

variable "category" {
  description = "Agent category"
  type        = string
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "model" {
  description = "AI model to use"
  type        = string
  default     = "gemini-2.0-flash-exp"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

# Vertex AI Agent Engine deployment
resource "google_vertex_ai_endpoint" "agent_endpoint" {
  name         = "${var.environment}-${var.agent_name}-endpoint"
  display_name = "${var.display_name} Agent - ${var.environment}"
  project      = var.project_id
  region       = var.region

  labels = {
    agent_id    = var.agent_id
    tier        = var.tier
    category    = var.category
    environment = var.environment
    managed_by  = "terraform"
  }
}

# Cloud Run service for agent runtime
resource "google_cloud_run_service" "agent_service" {
  name     = "${var.environment}-${var.agent_name}-service"
  location = var.region
  project  = var.project_id

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/saas-agents/${var.agent_name}:latest"

        env {
          name  = "AGENT_ID"
          value = var.agent_id
        }

        env {
          name  = "AGENT_NAME"
          value = var.agent_name
        }

        env {
          name  = "ENVIRONMENT"
          value = var.environment
        }

        env {
          name  = "MODEL"
          value = var.model
        }

        resources {
          limits = {
            cpu    = "2000m"
            memory = "4Gi"
          }
        }
      }

      service_account_name = google_service_account.agent_sa.email
    }

    metadata {
      labels = {
        agent_id    = var.agent_id
        tier        = var.tier
        category    = var.category
        environment = var.environment
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Service account for the agent
resource "google_service_account" "agent_sa" {
  account_id   = "${var.environment}-${var.agent_name}-sa"
  display_name = "${var.display_name} Agent Service Account"
  project      = var.project_id
}

# IAM bindings for service account
resource "google_project_iam_member" "agent_vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

resource "google_project_iam_member" "agent_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

resource "google_project_iam_member" "agent_monitoring" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

# Secret Manager for API keys
resource "google_secret_manager_secret" "agent_api_key" {
  secret_id = "${var.environment}-${var.agent_name}-api-key"
  project   = var.project_id

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "agent_secret_access" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.agent_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.agent_sa.email}"
}

# Monitoring alert policy
resource "google_monitoring_alert_policy" "agent_error_rate" {
  display_name = "${var.display_name} - High Error Rate"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "Error rate > 5%"

    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${google_cloud_run_service.agent_service.name}\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.05

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = var.notification_channels
}

variable "notification_channels" {
  description = "Notification channels for alerts"
  type        = list(string)
  default     = []
}

# Outputs
output "endpoint_name" {
  description = "Vertex AI endpoint name"
  value       = google_vertex_ai_endpoint.agent_endpoint.name
}

output "service_url" {
  description = "Cloud Run service URL"
  value       = google_cloud_run_service.agent_service.status[0].url
}

output "service_account_email" {
  description = "Service account email"
  value       = google_service_account.agent_sa.email
}
