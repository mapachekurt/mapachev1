# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Outputs for use in CI/CD pipelines and documentation

# Project IDs
output "cicd_project_id" {
  description = "CI/CD runner project ID"
  value       = var.cicd_runner_project_id
}

output "staging_project_id" {
  description = "Staging environment project ID"
  value       = var.staging_project_id
}

output "prod_project_id" {
  description = "Production environment project ID"
  value       = var.prod_project_id
}

# Service Account Emails
output "cicd_service_account_email" {
  description = "CI/CD runner service account email"
  value       = google_service_account.cicd_runner_sa.email
}

output "app_service_account_emails" {
  description = "Application service account emails by environment"
  value = {
    for env, project_id in local.deploy_project_ids :
    env => google_service_account.app_sa[env].email
  }
}

# Storage Resources
output "logs_buckets" {
  description = "GCS buckets for logs by project"
  value = {
    for project_id in local.all_project_ids :
    project_id => google_storage_bucket.logs_data_bucket[project_id].name
  }
}

output "trace_payload_buckets" {
  description = "GCS buckets for large trace payloads by environment"
  value = {
    for env, project_id in local.deploy_project_ids :
    env => google_storage_bucket.trace_payloads[env].name
  }
}

output "artifact_registry_repository" {
  description = "Artifact Registry repository for Docker images"
  value       = google_artifact_registry_repository.docker_repo.id
}

output "artifact_registry_url" {
  description = "Full URL for pushing Docker images"
  value       = "${var.region}-docker.pkg.dev/${var.cicd_runner_project_id}/${google_artifact_registry_repository.docker_repo.repository_id}"
}

# BigQuery Resources
output "telemetry_datasets" {
  description = "BigQuery datasets for telemetry logs by environment"
  value = {
    for env, project_id in local.deploy_project_ids :
    env => "${project_id}.${google_bigquery_dataset.telemetry_logs_dataset[env].dataset_id}"
  }
}

output "feedback_datasets" {
  description = "BigQuery datasets for feedback data by environment"
  value = {
    for env, project_id in local.deploy_project_ids :
    env => "${project_id}.${google_bigquery_dataset.feedback_dataset[env].dataset_id}"
  }
}

output "analytics_datasets" {
  description = "BigQuery datasets for analytics by environment"
  value = {
    for env, project_id in local.deploy_project_ids :
    env => "${project_id}.${google_bigquery_dataset.analytics[env].dataset_id}"
  }
}

output "evaluations_datasets" {
  description = "BigQuery datasets for agent evaluations by environment"
  value = {
    for env, project_id in local.deploy_project_ids :
    env => "${project_id}.${google_bigquery_dataset.evaluations[env].dataset_id}"
  }
}

# Monitoring Resources
output "monitoring_dashboards" {
  description = "Cloud Monitoring dashboard URLs by environment"
  value = {
    for env, project_id in local.deploy_project_ids :
    env => "https://console.cloud.google.com/monitoring/dashboards/custom/${google_monitoring_dashboard.agent_dashboard[env].id}?project=${project_id}"
  }
}

output "notification_channels" {
  description = "Monitoring notification channel IDs by environment"
  value = var.alert_email != "" && var.enable_alerts ? {
    for env, project_id in local.deploy_project_ids :
    env => google_monitoring_notification_channel.email[env].id
  } : {}
}

# Region and Configuration
output "region" {
  description = "GCP region for all resources"
  value       = var.region
}

output "project_name" {
  description = "Project name used for resource naming"
  value       = var.project_name
}

# Workload Identity Federation (if using GitHub Actions)
output "wif_provider_name" {
  description = "Workload Identity Federation provider name for GitHub Actions"
  value       = try(google_iam_workload_identity_pool_provider.github_provider[0].name, null)
}

output "wif_service_account" {
  description = "Service account email for Workload Identity Federation"
  value       = try(google_iam_workload_identity_pool_provider.github_provider[0].name, null) != null ? google_service_account.cicd_runner_sa.email : null
}

# Quick Access URLs
output "console_urls" {
  description = "Quick links to Google Cloud Console"
  value = {
    for env, project_id in local.deploy_project_ids :
    env => {
      project      = "https://console.cloud.google.com/home/dashboard?project=${project_id}"
      logs         = "https://console.cloud.google.com/logs/query?project=${project_id}"
      traces       = "https://console.cloud.google.com/traces/list?project=${project_id}"
      bigquery     = "https://console.cloud.google.com/bigquery?project=${project_id}&ws=!1m5!1m4!4m3!1s${project_id}!2s${google_bigquery_dataset.analytics[env].dataset_id}!3sagent_performance"
      monitoring   = "https://console.cloud.google.com/monitoring?project=${project_id}"
      cloud_run    = "https://console.cloud.google.com/run?project=${project_id}"
    }
  }
}

# Summary output for easy reference
output "deployment_summary" {
  description = "Summary of deployed infrastructure"
  value = <<-EOT

    ========================================
    Multi-Agent System Infrastructure
    ========================================

    Project Name: ${var.project_name}
    Region: ${var.region}

    ENVIRONMENTS:
    - Staging: ${var.staging_project_id}
    - Production: ${var.prod_project_id}
    - CI/CD Runner: ${var.cicd_runner_project_id}

    SERVICE ACCOUNTS:
    - CI/CD: ${google_service_account.cicd_runner_sa.email}
    - App (Staging): ${google_service_account.app_sa["staging"].email}
    - App (Production): ${google_service_account.app_sa["prod"].email}

    ARTIFACT REGISTRY:
    - Repository: ${google_artifact_registry_repository.docker_repo.repository_id}
    - Push URL: ${var.region}-docker.pkg.dev/${var.cicd_runner_project_id}/${google_artifact_registry_repository.docker_repo.repository_id}

    BIGQUERY DATASETS:
    - Telemetry (Staging): ${var.staging_project_id}.${google_bigquery_dataset.telemetry_logs_dataset["staging"].dataset_id}
    - Telemetry (Prod): ${var.prod_project_id}.${google_bigquery_dataset.telemetry_logs_dataset["prod"].dataset_id}
    - Analytics (Staging): ${var.staging_project_id}.${google_bigquery_dataset.analytics["staging"].dataset_id}
    - Analytics (Prod): ${var.prod_project_id}.${google_bigquery_dataset.analytics["prod"].dataset_id}

    NEXT STEPS:
    1. Configure CI/CD pipeline with these outputs
    2. Set up GitHub Actions secrets or Cloud Build triggers
    3. Deploy your agent to staging for testing
    4. Review monitoring dashboards and set up alerts
    5. Promote to production after validation

    ========================================
  EOT
}
