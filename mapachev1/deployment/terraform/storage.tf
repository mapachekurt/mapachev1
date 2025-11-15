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

provider "google" {
  region = var.region
  user_project_override = true
}

# GCS bucket for Cloud Build and general logs
resource "google_storage_bucket" "logs_data_bucket" {
  for_each                    = toset(local.all_project_ids)
  name                        = "${each.value}-${var.project_name}-logs"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true

  lifecycle_rule {
    condition {
      age = 30 # days
    }
    action {
      type = "Delete"
    }
  }

  labels = {
    purpose    = "logs"
    managed_by = "terraform"
  }

  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}

# Artifact Registry for Docker images (in CI/CD project)
resource "google_artifact_registry_repository" "docker_repo" {
  project       = var.cicd_runner_project_id
  location      = var.region
  repository_id = "${var.project_name}-docker"
  description   = "Docker repository for ${var.project_name} multi-agent system"
  format        = "DOCKER"

  labels = {
    purpose    = "container-images"
    managed_by = "terraform"
  }

  depends_on = [resource.google_project_service.cicd_services]
}

# Grant Cloud Run service agents access to pull images from Artifact Registry
resource "google_artifact_registry_repository_iam_member" "cloud_run_artifact_reader" {
  for_each = local.deploy_project_ids

  project    = var.cicd_runner_project_id
  location   = var.region
  repository = google_artifact_registry_repository.docker_repo.repository_id
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:service-${data.google_project.projects[each.key].number}@serverless-robot-prod.iam.gserviceaccount.com"

  depends_on = [google_artifact_registry_repository.docker_repo, data.google_project.projects]
}

# GCS bucket for large trace payloads (>256KB spans)
# These are referenced from Cloud Logging entries when spans are too large
resource "google_storage_bucket" "trace_payloads" {
  for_each = local.deploy_project_ids

  name                        = "${each.value}-${var.project_name}-trace-payloads"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true

  # Lifecycle: Delete trace payloads after 7 days (they're for debugging, not long-term storage)
  lifecycle_rule {
    condition {
      age = 7 # days
    }
    action {
      type = "Delete"
    }
  }

  # Auto-transition to Nearline after 1 day (cheaper storage for infrequent access)
  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  labels = {
    purpose     = "trace-payloads"
    environment = each.key
    managed_by  = "terraform"
  }

  depends_on = [resource.google_project_service.deploy_project_services]
}

# Grant application service accounts write access to trace payload buckets
resource "google_storage_bucket_iam_member" "app_sa_trace_bucket_writer" {
  for_each = local.deploy_project_ids

  bucket = google_storage_bucket.trace_payloads[each.key].name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.app_sa[each.key].email}"

  depends_on = [google_storage_bucket.trace_payloads, google_service_account.app_sa]
}

# GCS bucket for agent data ingestion pipelines (optional, if using RAG)
resource "google_storage_bucket" "data_ingestion" {
  for_each = local.deploy_project_ids

  name                        = "${each.value}-${var.project_name}-data-ingestion"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = false # Don't auto-delete data

  versioning {
    enabled = true
  }

  labels = {
    purpose     = "data-ingestion"
    environment = each.key
    managed_by  = "terraform"
  }

  depends_on = [resource.google_project_service.deploy_project_services]
}

# Grant application service accounts admin access to data ingestion buckets
resource "google_storage_bucket_iam_member" "app_sa_data_bucket_admin" {
  for_each = local.deploy_project_ids

  bucket = google_storage_bucket.data_ingestion[each.key].name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.app_sa[each.key].email}"

  depends_on = [google_storage_bucket.data_ingestion, google_service_account.app_sa]
}



