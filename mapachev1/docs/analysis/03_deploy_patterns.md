# Agent Starter Pack: Complete Deployment Patterns Documentation

**Generated:** November 14, 2025  
**Repository:** Agent Starter Pack  
**Scope:** Comprehensive analysis of ALL deployment patterns across Terraform, CI/CD pipelines, and multi-environment infrastructure

---

## Table of Contents

1. [Overview](#overview)
2. [Terraform Infrastructure Structure](#terraform-infrastructure-structure)
3. [Multi-Environment Setup](#multi-environment-setup)
4. [CI/CD Pipeline Architecture](#cicd-pipeline-architecture)
5. [Service Accounts and IAM Configuration](#service-accounts-and-iam-configuration)
6. [Secret Management](#secret-management)
7. [Staging to Production Promotion Workflow](#staging-to-production-promotion-workflow)
8. [Agent Engine Deployment Process](#agent-engine-deployment-process)
9. [Cloud Run Deployment Process](#cloud-run-deployment-process)
10. [Deployment Commands and Automation](#deployment-commands-and-automation)
11. [Environment-Specific Configurations](#environment-specific-configurations)
12. [Logging and Observability](#logging-and-observability)

---

## Overview

The Agent Starter Pack provides a production-ready deployment infrastructure using:

- **Infrastructure as Code:** HashiCorp Terraform (v1.0+)
- **CI/CD Runners:** Google Cloud Build OR GitHub Actions (selectable during project creation)
- **Multi-Environment Support:** Development, Staging, and Production
- **Container Registry:** Google Cloud Artifact Registry (for Cloud Run deployments)
- **Service Accounts:** Granular IAM roles for security and least privilege
- **Observability:** BigQuery log sinks for telemetry and feedback data
- **State Management:** Google Cloud Storage backend for Terraform state

### Key Features

- **Infrastructure Provisioning:** Automated via Terraform with environment-specific configurations
- **Automated Testing:** Unit tests, integration tests, and E2E deployment tests
- **Safe Deployments:** Staging environment for validation before production promotion
- **Manual Approval Gates:** Production deployments require explicit approval
- **Multiple Deployment Targets:** Cloud Run (container-based) and Agent Engine (serverless execution)
- **Data Ingestion Support:** Optional Vertex AI Pipelines for scheduled data processing

---

## Terraform Infrastructure Structure

### Directory Organization

```
agent_starter_pack/
├── base_template/
│   └── deployment/
│       └── terraform/
│           ├── providers.tf           # Provider configuration
│           ├── variables.tf           # Variable definitions
│           ├── locals.tf              # Local value definitions
│           ├── service_accounts.tf    # Service account creation
│           ├── iam.tf                 # IAM role assignments
│           ├── apis.tf                # GCP API enablement
│           ├── storage.tf             # Storage buckets, vector search, discovery engine
│           ├── log_sinks.tf           # BigQuery log sinks for telemetry
│           ├── github.tf              # GitHub integration (variables & secrets)
│           ├── dev/
│           │   ├── providers.tf       # Dev provider aliases
│           │   ├── variables.tf       # Dev-specific variables
│           │   ├── iam.tf             # Dev IAM configuration
│           │   ├── apis.tf            # Dev APIs
│           │   ├── storage.tf         # Dev storage resources
│           │   ├── log_sinks.tf       # Dev logging
│           │   └── vars/
│           │       └── env.tfvars     # Dev environment variables
│           └── vars/
│               └── env.tfvars         # Staging/Prod environment variables
├── deployment_targets/
│   └── cloud_run/
│       └── deployment/
│           └── terraform/
│               ├── service.tf         # Cloud Run service definition
│               └── dev/
│                   └── service.tf     # Dev Cloud Run service
└── (other deployment targets)

.cloudbuild/
├── terraform/
│   ├── variables.tf                  # CI/CD infrastructure variables
│   ├── service_account.tf            # CI/CD runner service account
│   ├── build_triggers.tf             # Cloud Build trigger definitions
│   ├── storage.tf                    # CI/CD logs bucket
│   ├── apis.tf                       # CI/CD APIs
│   ├── backend.tf                    # Terraform state backend
│   └── scheduled_cleanup.tf          # Resource cleanup automation
├── ci/
│   ├── test.yaml                     # Unit tests Cloud Build configuration
│   ├── lint.yaml                     # Code linting Cloud Build configuration
│   ├── test_templated_agents.yaml    # Agent template testing
│   ├── lint_templated_agents.yaml    # Agent template linting
│   ├── test_remote_template.yaml     # Remote template testing
│   ├── test_makefile.yaml            # Makefile usability testing
│   ├── test_pipeline_parity.yaml     # GitHub Actions vs Cloud Build parity
│   └── build_use_wheel.yaml          # Wheel build testing
├── cd/
│   ├── test_e2e.yaml                 # End-to-end deployment tests
│   └── test_gemini_enterprise.yaml   # Gemini Enterprise registration tests
└── scheduled-cleanup.yaml            # Scheduled cleanup triggers
```

### Core Terraform Files Structure

#### 1. **providers.tf** - Provider Configuration

```hcl
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.10.0"
    }
    github = {
      source  = "integrations/github"
      version = "~> 6.5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7.0"
    }
  }
}

# Provider aliases for staging and production billing overrides
provider "google" {
  alias                 = "staging_billing_override"
  billing_project       = var.staging_project_id
  region                = var.region
  user_project_override = true
}

provider "google" {
  alias                 = "prod_billing_override"
  billing_project       = var.prod_project_id
  region                = var.region
  user_project_override = true
}
```

**Purpose:** Configures Terraform to work with multiple GCP projects simultaneously using provider aliases, enabling billing project overrides for each environment.

#### 2. **variables.tf** - Variable Definitions

```hcl
# Core Configuration
variable "project_name" {
  type        = string
  description = "Project name used as a base for resource naming"
}

variable "prod_project_id" {
  type        = string
  description = "**Production** Google Cloud Project ID"
}

variable "staging_project_id" {
  type        = string
  description = "**Staging** Google Cloud Project ID"
}

variable "cicd_runner_project_id" {
  type        = string
  description = "Project ID where CI/CD pipelines execute"
}

variable "region" {
  type        = string
  description = "Google Cloud region for resource deployment"
  default     = "us-central1"
}

# Service Account Roles - Application
variable "app_sa_roles" {
  description = "Roles for application service account"
  type        = list(string)
  default = [
    "roles/aiplatform.user",           # AI Platform access
    "roles/discoveryengine.editor",    # Discovery Engine access
    "roles/logging.logWriter",         # Write logs
    "roles/cloudtrace.agent",          # Cloud Trace agent
    "roles/storage.admin",             # Storage access
    "roles/serviceusage.serviceUsageConsumer"
  ]
}

# Service Account Roles - CI/CD Runner
variable "cicd_roles" {
  description = "Roles for CI/CD runner in CICD project"
  type        = list(string)
  default = [
    "roles/run.invoker",               # Invoke Cloud Run services
    "roles/storage.admin",
    "roles/aiplatform.user",
    "roles/discoveryengine.editor",
    "roles/logging.logWriter",
    "roles/cloudtrace.agent",
    "roles/artifactregistry.writer",   # Push container images
    "roles/cloudbuild.builds.builder"
  ]
}

# Service Account Roles - CI/CD Deployment to Staging/Prod
variable "cicd_sa_deployment_required_roles" {
  description = "Roles for CI/CD deployment in Staging and Prod"
  type        = list(string)
  default = [
    "roles/run.developer",             # Deploy Cloud Run services
    "roles/iam.serviceAccountUser",    # Impersonate app service account
    "roles/aiplatform.user",
    "roles/storage.admin"
  ]
}

# Optional: Data Ingestion Pipeline Roles
variable "pipelines_roles" {
  description = "Roles for Vertex AI Pipelines service account"
  type        = list(string)
  default = [
    "roles/storage.admin",
    "roles/aiplatform.user",
    "roles/discoveryengine.admin",
    "roles/logging.logWriter",
    "roles/artifactregistry.writer",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/bigquery.readSessionUser",
    "roles/bigquery.connectionAdmin",
    "roles/resourcemanager.projectIamAdmin"
  ]
}
```

#### 3. **locals.tf** - Local Values

```hcl
locals {
  # CI/CD project services
  cicd_services = [
    "cloudbuild.googleapis.com",
    "discoveryengine.googleapis.com",
    "aiplatform.googleapis.com",
    "serviceusage.googleapis.com",
    "bigquery.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudtrace.googleapis.com"
  ]

  # Deployment (Staging/Prod) project services
  deploy_project_services = [
    "aiplatform.googleapis.com",
    "run.googleapis.com",                # Cloud Run
    "discoveryengine.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "bigquery.googleapis.com",           # For log sinks
    "serviceusage.googleapis.com",
    "logging.googleapis.com",
    "cloudtrace.googleapis.com",
    "compute.googleapis.com",            # For AlloyDB networking
    "servicenetworking.googleapis.com",  # For AlloyDB networking
    "alloydb.googleapis.com",            # For AlloyDB sessions
    "secretmanager.googleapis.com"       # For secrets
  ]

  # Deployment project mapping
  deploy_project_ids = {
    prod    = var.prod_project_id
    staging = var.staging_project_id
  }

  # All project IDs for looping
  all_project_ids = [
    var.cicd_runner_project_id,
    var.prod_project_id,
    var.staging_project_id
  ]
}
```

#### 4. **service_accounts.tf** - Service Account Creation

```hcl
# CI/CD Runner Service Account
resource "google_service_account" "cicd_runner_sa" {
  account_id   = "${var.project_name}-cb"
  display_name = "CICD Runner SA"
  project      = var.cicd_runner_project_id
  depends_on   = [resource.google_project_service.cicd_services]
}

# Application Service Account (Staging & Prod)
resource "google_service_account" "app_sa" {
  for_each = local.deploy_project_ids

  account_id   = "${var.project_name}-app"
  display_name = "${var.project_name} Agent Service Account"
  project      = each.value
  depends_on   = [resource.google_project_service.deploy_project_services]
}

# Data Ingestion Service Account (Optional)
resource "google_service_account" "vertexai_pipeline_app_sa" {
  for_each = local.deploy_project_ids

  account_id   = "${var.project_name}-rag"
  display_name = "Vertex AI Pipeline SA"
  project      = each.value
  depends_on   = [resource.google_project_service.deploy_project_services]
}
```

#### 5. **iam.tf** - IAM Role Assignments

The IAM configuration implements a sophisticated permission model:

```hcl
# 1. CI/CD project roles
resource "google_project_iam_member" "cicd_project_roles" {
  for_each = toset(var.cicd_roles)

  project = var.cicd_runner_project_id
  role    = each.value
  member  = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
}

# 2. Staging/Prod deployment roles
resource "google_project_iam_member" "other_projects_roles" {
  for_each = {
    for pair in setproduct(keys(local.deploy_project_ids), var.cicd_sa_deployment_required_roles) :
    "${pair[0]}-${pair[1]}" => {
      project_id = local.deploy_project_ids[pair[0]]
      role       = pair[1]
    }
  }

  project = each.value.project_id
  role    = each.value.role
  member  = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
}

# 3. Application service account permissions
resource "google_project_iam_member" "app_sa_roles" {
  for_each = {
    for pair in setproduct(keys(local.deploy_project_ids), var.app_sa_roles) :
    join(",", pair) => {
      project = local.deploy_project_ids[pair[0]]
      role    = pair[1]
    }
  }

  project = each.value.project
  role    = each.value.role
  member  = "serviceAccount:${google_service_account.app_sa[split(",", each.key)[0]].email}"
}

# 4. Cloud Run <-> Artifact Registry access
resource "google_project_iam_member" "cicd_run_invoker_artifact_registry_reader" {
  for_each = local.deploy_project_ids
  project  = var.cicd_runner_project_id

  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:service-${data.google_project.projects[each.key].number}@serverless-robot-prod.iam.gserviceaccount.com"
}

# 5. Token creator for service account impersonation
resource "google_service_account_iam_member" "cicd_run_invoker_token_creator" {
  service_account_id = google_service_account.cicd_runner_sa.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
}

# 6. Data ingestion pipeline permissions
resource "google_project_iam_member" "vertexai_pipeline_sa_roles" {
  for_each = {
    for pair in setproduct(keys(local.deploy_project_ids), var.pipelines_roles) :
    join(",", pair) => {
      project = local.deploy_project_ids[pair[0]]
      role    = pair[1]
    }
  }

  project = each.value.project
  role    = each.value.role
  member  = "serviceAccount:${google_service_account.vertexai_pipeline_app_sa[split(",", each.key)[0]].email}"
}
```

#### 6. **apis.tf** - GCP API Enablement

```hcl
# Enable APIs in CI/CD project
resource "google_project_service" "cicd_services" {
  count              = length(local.cicd_services)
  project            = var.cicd_runner_project_id
  service            = local.cicd_services[count.index]
  disable_on_destroy = false
}

# Enable APIs in Staging/Prod projects
resource "google_project_service" "deploy_project_services" {
  for_each = {
    for pair in setproduct(keys(local.deploy_project_ids), local.deploy_project_services) :
    "${pair[0]}_${replace(pair[1], ".", "_")}" => {
      project = local.deploy_project_ids[pair[0]]
      service = pair[1]
    }
  }
  project            = each.value.project
  service            = each.value.service
  disable_on_destroy = false
}
```

#### 7. **storage.tf** - Storage Resources

```hcl
# Logs bucket in all projects
resource "google_storage_bucket" "logs_data_bucket" {
  for_each                    = toset(local.all_project_ids)
  name                        = "${each.value}-${var.project_name}-logs"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true
}

# Artifact Registry for Cloud Run container images
resource "google_artifact_registry_repository" "repo-artifacts-genai" {
  location      = var.region
  repository_id = "${var.project_name}-repo"
  description   = "Container image repository for AI applications"
  format        = "DOCKER"
  project       = var.cicd_runner_project_id
}

# Data ingestion pipeline bucket
resource "google_storage_bucket" "data_ingestion_pipeline_gcs_root" {
  for_each                    = local.deploy_project_ids
  name                        = "${each.value}-${var.project_name}-rag"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true
}

# Vector Search bucket
resource "google_storage_bucket" "vector_search_data_bucket" {
  for_each                    = local.deploy_project_ids
  name                        = "${each.value}-${var.project_name}-vs"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true
}
```

#### 8. **log_sinks.tf** - Observability and Telemetry

```hcl
# BigQuery datasets for storing logs
resource "google_bigquery_dataset" "feedback_dataset" {
  for_each      = local.deploy_project_ids
  project       = each.value
  dataset_id    = replace("${var.project_name}_feedback", "-", "_")
  friendly_name = "${var.project_name}_feedback"
  location      = var.region
}

resource "google_bigquery_dataset" "telemetry_logs_dataset" {
  for_each      = local.deploy_project_ids
  project       = each.value
  dataset_id    = replace("${var.project_name}_telemetry", "-", "_")
  friendly_name = "${var.project_name}_telemetry"
  location      = var.region
}

# Log sinks for feedback data
resource "google_logging_project_sink" "feedback_export_to_bigquery" {
  for_each = local.deploy_project_ids

  name        = "${var.project_name}_feedback"
  project     = each.value
  destination = "bigquery.googleapis.com/projects/${each.value}/datasets/${google_bigquery_dataset.feedback_dataset[each.key].dataset_id}"
  filter      = var.feedback_logs_filter  # Default: jsonPayload.log_type="feedback"

  bigquery_options {
    use_partitioned_tables = true
  }
  unique_writer_identity = true
}

# Log sinks for telemetry data
resource "google_logging_project_sink" "log_export_to_bigquery" {
  for_each = local.deploy_project_ids

  name        = "${var.project_name}_telemetry"
  project     = each.value
  destination = "bigquery.googleapis.com/projects/${each.value}/datasets/${google_bigquery_dataset.telemetry_logs_dataset[each.key].dataset_id}"
  filter      = var.telemetry_logs_filter  # Default: traceloop association properties

  bigquery_options {
    use_partitioned_tables = true
  }
  unique_writer_identity = true
}

# Grant BigQuery Data Editor role to log sinks
resource "google_project_iam_member" "bigquery_data_editor" {
  for_each = local.deploy_project_ids

  project = each.value
  role    = "roles/bigquery.dataEditor"
  member  = google_logging_project_sink.log_export_to_bigquery[each.key].writer_identity
}
```

#### 9. **github.tf** - GitHub Integration

For **GitHub Actions** (WIF-based):

```hcl
provider "github" {
  owner = var.repository_owner
}

# Create GitHub repository
resource "github_repository" "repo" {
  count       = var.create_repository ? 1 : 0
  name        = var.repository_name
  description = "Repository created with Agent Starter Pack"
  visibility  = "private"
  has_issues  = true
  has_wiki    = false
}

# Set GitHub Actions variables (secrets and non-secrets)
resource "github_actions_variable" "gcp_project_number" {
  repository    = var.repository_name
  variable_name = "GCP_PROJECT_NUMBER"
  value         = data.google_project.cicd_project.number
}

resource "github_actions_secret" "wif_pool_id" {
  repository      = var.repository_name
  secret_name     = "WIF_POOL_ID"
  plaintext_value = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
}

resource "github_actions_secret" "wif_provider_id" {
  repository      = var.repository_name
  secret_name     = "WIF_PROVIDER_ID"
  plaintext_value = google_iam_workload_identity_pool_provider.github_provider.workload_identity_pool_provider_id
}

resource "github_actions_secret" "gcp_service_account" {
  repository      = var.repository_name
  secret_name     = "GCP_SERVICE_ACCOUNT"
  plaintext_value = google_service_account.cicd_runner_sa.email
}

# Project ID variables
resource "github_actions_variable" "staging_project_id" {
  repository    = var.repository_name
  variable_name = "STAGING_PROJECT_ID"
  value         = var.staging_project_id
}

resource "github_actions_variable" "prod_project_id" {
  repository    = var.repository_name
  variable_name = "PROD_PROJECT_ID"
  value         = var.prod_project_id
}

# Environment-specific variables
resource "github_actions_variable" "app_sa_email_staging" {
  repository    = var.repository_name
  variable_name = "APP_SA_EMAIL_STAGING"
  value         = google_service_account.app_sa["staging"].email
}

resource "github_actions_variable" "app_sa_email_prod" {
  repository    = var.repository_name
  variable_name = "APP_SA_EMAIL_PROD"
  value         = google_service_account.app_sa["prod"].email
}

# For Cloud Run deployments
resource "github_actions_variable" "container_name" {
  repository    = var.repository_name
  variable_name = "CONTAINER_NAME"
  value         = var.project_name
}

resource "github_actions_variable" "artifact_registry_repo_name" {
  repository    = var.repository_name
  variable_name = "ARTIFACT_REGISTRY_REPO_NAME"
  value         = google_artifact_registry_repository.repo-artifacts-genai.repository_id
}

# For data ingestion pipelines
resource "github_actions_variable" "pipeline_gcs_root_staging" {
  repository    = var.repository_name
  variable_name = "PIPELINE_GCS_ROOT_STAGING"
  value         = "gs://${google_storage_bucket.data_ingestion_pipeline_gcs_root["staging"].name}"
}

# Production environment configuration
resource "github_repository_environment" "production_environment" {
  repository  = var.repository_name
  environment = "production"

  deployment_branch_policy {
    protected_branches     = false
    custom_branch_policies = true
  }
}
```

For **Cloud Build** (PAT-based):

```hcl
# Reference existing GitHub PAT secret
data "google_secret_manager_secret" "github_pat" {
  project   = var.cicd_runner_project_id
  secret_id = var.github_pat_secret_id
}

# Grant Cloud Build service account access to PAT secret
resource "google_secret_manager_secret_iam_member" "cloudbuild_secret_accessor" {
  project   = var.cicd_runner_project_id
  secret_id = data.google_secret_manager_secret.github_pat.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:service-${data.google_project.cicd_project.number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
}

# Create Cloud Build GitHub connection
resource "google_cloudbuildv2_connection" "github_connection" {
  count    = var.create_cb_connection ? 0 : 1
  project  = var.cicd_runner_project_id
  location = var.region
  name     = var.host_connection_name

  github_config {
    app_installation_id = var.github_app_installation_id
    authorizer_credential {
      oauth_token_secret_version = "${data.google_secret_manager_secret.github_pat.id}/versions/latest"
    }
  }
}

# Register repository with Cloud Build
resource "google_cloudbuildv2_repository" "repo" {
  project  = var.cicd_runner_project_id
  location = var.region
  name     = var.repository_name
  
  parent_connection = var.create_cb_connection ? 
    "projects/${var.cicd_runner_project_id}/locations/${var.region}/connections/${var.host_connection_name}" : 
    google_cloudbuildv2_connection.github_connection[0].id
  
  remote_uri = "https://github.com/${var.repository_owner}/${var.repository_name}.git"
}
```

---

## Multi-Environment Setup

### Development Environment (Dev)

**Purpose:** Local development and testing on a dedicated GCP project

**Structure:**
- Dedicated project ID: `var.dev_project_id`
- Minimal resource configuration for cost optimization
- Single environment (no staging/prod separation)

**Resources Created:**
- Single Cloud Run service or Agent Engine deployment
- Single app service account
- Storage buckets for logs and data ingestion
- Discovery Engine datastore (if using Vertex AI Search)
- Vector Search index (if using Vector Search)
- AlloyDB cluster (if using AlloyDB sessions)

**Dev Terraform Configuration:**

```hcl
# Development environment structure
terraform/
├── dev/
│   ├── providers.tf
│   ├── variables.tf
│   ├── iam.tf
│   ├── apis.tf
│   ├── storage.tf
│   ├── log_sinks.tf (same pattern as prod/staging)
│   └── vars/
│       └── env.tfvars
```

**Dev-Specific Variables:**

```hcl
variable "dev_project_id" {
  type        = string
  description = "Dev Google Cloud Project ID"
}

variable "app_sa_roles" {
  description = "Application service account roles"
  type        = list(string)
  default = [
    "roles/aiplatform.user",
    "roles/discoveryengine.editor",
    "roles/logging.logWriter",
    "roles/cloudtrace.agent",
    "roles/storage.admin",
    "roles/serviceusage.serviceUsageConsumer",
  ]
}

variable "pipelines_roles" {
  description = "Data ingestion pipeline roles"
  type        = list(string)
  default = [
    "roles/storage.admin",
    "roles/run.invoker",
    "roles/aiplatform.user",
    "roles/discoveryengine.admin",
    "roles/logging.logWriter",
    "roles/artifactregistry.writer",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
  ]
}
```

**Key Differences from Staging/Prod:**
- Uses `for_each` over a single `{ dev = var.dev_project_id }` map
- No separate staging/prod provider aliases needed
- Single App SA instead of for_each loop
- Simpler API enabling with local services list

### Staging Environment

**Purpose:** Pre-production validation with production-like configuration

**Resources:**
- App service account for staging
- Cloud Run service with 1-10 instance scaling
- BigQuery datasets for telemetry and feedback
- Discovery Engine or Vector Search datastore
- Same logging and observability as production

### Production Environment

**Purpose:** Live agent service with maximum reliability and performance

**Resources:**
- App service account for production
- Cloud Run service with 1-10 instance scaling
- Production BigQuery datasets
- Production Discovery Engine or Vector Search datastore
- Full observability and audit logging

### Environment Projection Pattern

The Terraform code uses a consistent pattern for managing multiple environments:

```hcl
locals {
  deploy_project_ids = {
    prod    = var.prod_project_id
    staging = var.staging_project_id
  }
}

# Loop over environments
resource "google_service_account" "app_sa" {
  for_each = local.deploy_project_ids

  account_id   = "${var.project_name}-app"
  display_name = "${var.project_name} Agent Service Account"
  project      = each.value
}

# Create resources for each environment
resource "google_cloud_run_v2_service" "app" {
  for_each = local.deploy_project_ids

  name     = var.project_name
  location = var.region
  project  = each.value
  # ... service configuration
}
```

This pattern ensures consistent resource naming and configuration across environments while maintaining separate state.

---

## CI/CD Pipeline Architecture

### Overview

The Agent Starter Pack supports two CI/CD runners with equivalent capabilities:

1. **Google Cloud Build** - Native GCP integration
2. **GitHub Actions** - GitHub-native workflows

**Both support:**
- Pull request checks (unit tests, linting, integration tests)
- Staging deployment on merge to main
- Production deployment with manual approval
- E2E deployment testing
- Scheduled cleanup jobs

### Cloud Build Architecture

#### Build Triggers

The Cloud Build infrastructure is defined in `.cloudbuild/terraform/build_triggers.tf` and creates multiple triggers:

```hcl
locals {
  # Trigger naming and organization
  trigger_name_safe = { for combo in local.agent_testing_combinations :
    combo.name => replace(replace(combo.name, "_", "-"), ".", "-")
  }

  # Tested agent/deployment combinations
  agent_testing_combinations = [
    { name = "adk_base-agent_engine", value = "adk_base,agent_engine" },
    { name = "adk_base-cloud_run", value = "adk_base,cloud_run" },
    { name = "langgraph_base_react-agent_engine", value = "langgraph_base_react,agent_engine" },
    { name = "langgraph_base_react-cloud_run", value = "langgraph_base_react,cloud_run,-dir,tag" },
    { name = "agentic_rag-agent_engine-vertex_ai_search", value = "agentic_rag,agent_engine,--include-data-ingestion,--datastore,vertex_ai_search" },
    # ... more combinations
  ]
}
```

#### Trigger Types

**1. PR Checks (Pull Request Events)**

```hcl
resource "google_cloudbuild_trigger" "pr_tests" {
  name            = "pr-tests"
  project         = var.cicd_runner_project_id
  location        = var.region
  description     = "Unit and integration tests on PR"
  service_account = resource.google_service_account.cicd_runner_sa.id

  repository_event_config {
    repository = local.repository_path
    pull_request {
      branch          = "main"
      comment_control = "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"
    }
  }

  filename       = ".cloudbuild/ci/test.yaml"
  included_files = local.common_included_files
  ignored_files  = ["**/*.md", "**/Makefile"]
  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"
}
```

**2. Lint Triggers (Code Quality)**

```hcl
resource "google_cloudbuild_trigger" "pr_lint" {
  name            = "pr-lint"
  project         = var.cicd_runner_project_id
  location        = var.region
  service_account = resource.google_service_account.cicd_runner_sa.id

  repository_event_config {
    repository = local.repository_path
    pull_request {
      branch          = "main"
      comment_control = "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"
    }
  }

  filename       = ".cloudbuild/ci/lint.yaml"
  included_files = local.common_included_files
}
```

**3. E2E Deployment Tests (Main Branch)**

```hcl
resource "google_cloudbuild_trigger" "main_e2e_deployment_test" {
  for_each = { for combo in local.e2e_agent_deployment_combinations : combo.name => combo }

  name            = "e2e-deploy-${local.e2e_trigger_name_safe[each.key]}"
  project         = var.cicd_runner_project_id
  location        = var.region
  service_account = resource.google_service_account.cicd_runner_sa.id

  repository_event_config {
    repository = local.repository_path
    push {
      branch = "main"
    }
  }

  filename       = ".cloudbuild/cd/test_e2e.yaml"
  included_files = local.e2e_agent_deployment_included_files[each.key]
  
  substitutions = {
    _TEST_AGENT_COMBINATION = each.value.value
    _E2E_DEV_PROJECT     = var.e2e_test_project_mapping.dev
    _E2E_STAGING_PROJECT = var.e2e_test_project_mapping.staging
    _E2E_PROD_PROJECT    = var.e2e_test_project_mapping.prod
  }
}
```

#### CI/CD Pipeline Configurations

**.cloudbuild/ci/test.yaml - Unit Tests**

```yaml
steps:
  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: install-dependencies
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        uv sync --dev --locked

  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: unit-tests
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        uv run pytest tests

logsBucket: gs://${PROJECT_ID}-logs-data/build-logs
options:
  defaultLogsBucketBehavior: REGIONAL_USER_OWNED_BUCKET
```

**.cloudbuild/ci/lint.yaml - Code Linting**

```yaml
steps:
  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: install-dependencies
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        uv sync --dev --extra lint --locked

  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: lint
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        set -e
        uv run ruff check . --config pyproject.toml --diff
        uv run ruff format . --check --config pyproject.toml --diff
        uv run mypy --config-file pyproject.toml ./agent_starter_pack/cli ./tests ./agent_starter_pack/frontends/streamlit

logsBucket: gs://${PROJECT_ID}-logs-data/build-logs
```

**.cloudbuild/cd/test_e2e.yaml - E2E Deployment Tests**

```yaml
steps:
  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: install-dependencies
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        uv sync --dev --locked

  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: e2e-tests
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        GH_TOKEN=$$GITHUB_PAT uv run pytest tests/cicd/test_e2e_deployment.py -v
    secretEnv: ['GITHUB_PAT', 'GITHUB_APP_INSTALLATION_ID']
    
availableSecrets:
  secretManager:
    - versionName: projects/$PROJECT_ID/secrets/github-pat/versions/latest
      env: 'GITHUB_PAT'
    - versionName: projects/$PROJECT_ID/secrets/github-app-installation-id/versions/latest
      env: 'GITHUB_APP_INSTALLATION_ID'

options:
  env:
    - "_TEST_AGENT_COMBINATION=${_TEST_AGENT_COMBINATION}"
    - "E2E_DEV_PROJECT=${_E2E_DEV_PROJECT}"
    - "E2E_STAGING_PROJECT=${_E2E_STAGING_PROJECT}"
    - "E2E_PROD_PROJECT=${_E2E_PROD_PROJECT}"
    - "E2E_CICD_PROJECT=${PROJECT_ID}"
    - "RUN_E2E_TESTS=1"

timeout: 43200s  # 12 hours for full deployment cycle
```

**.cloudbuild/scheduled-cleanup.yaml - Resource Cleanup**

```yaml
steps:
  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: force-cleanup
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        chmod +x tests/cicd/scripts/force-cleanup.sh
        ./tests/cicd/scripts/force-cleanup.sh

timeout: 18000s  # 5 hours for cleanup
logsBucket: gs://${PROJECT_ID}-logs-data/build-logs
```

### GitHub Actions Architecture

#### Workflow Structure

The template generates GitHub Actions workflows when `--cicd-runner github_actions` is selected:

```
.github/workflows/
├── pr_checks.yaml         # Pull request validation
├── staging.yaml           # Staging deployment on merge
└── deploy-to-prod.yaml    # Production deployment
```

#### Workload Identity Federation (WIF) Configuration

GitHub Actions uses WIF for secure authentication without long-lived credentials:

```hcl
# WIF Pool
resource "google_iam_workload_identity_pool" "github_pool" {
  project           = var.cicd_runner_project_id
  location          = "global"
  display_name      = "GitHub Actions Pool"
  workload_identity_pool_id = "github-pool"
}

# WIF Provider
resource "google_iam_workload_identity_pool_provider" "github_provider" {
  project = var.cicd_runner_project_id
  location          = "global"
  workload_identity_pool_id = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  display_name      = "GitHub Provider"
  workload_identity_pool_provider_id = "github-provider"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.aud"        = "assertion.aud"
    "attribute.repository" = "assertion.repository"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Service account IAM binding
resource "google_service_account_iam_member" "github_actions_sa_user" {
  service_account_id = google_service_account.cicd_runner_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/projects/${data.google_project.cicd_project.number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github_pool.workload_identity_pool_id}/attribute.repository/${var.repository_owner}/${var.repository_name}"
}
```

#### WIF Token Exchange in Workflows

```yaml
- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/${{ env.GCP_PROJECT_NUMBER }}/locations/global/workloadIdentityPools/${{ secrets.WIF_POOL_ID }}/providers/${{ secrets.WIF_PROVIDER_ID }}
    service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}
```

---

## Service Accounts and IAM Configuration

### Service Account Hierarchy

The deployment creates a three-tier service account structure:

```
┌─────────────────────────────────────────────────────────┐
│ CI/CD Project (cicd_runner_project_id)                 │
├─────────────────────────────────────────────────────────┤
│ Service Account: {project_name}-cb                     │
│ Roles:                                                  │
│  • roles/owner (in CICD project)                       │
│  • roles/run.invoker                                   │
│  • roles/storage.admin                                 │
│  • roles/aiplatform.user                               │
│  • roles/artifactregistry.writer                       │
│  • roles/cloudbuild.builds.builder                     │
└─────────────────────────────────────────────────────────┘
            ↓ Cross-project roles in Staging/Prod
┌─────────────────────────────────────────────────────────┐
│ Staging/Prod Projects                                   │
├─────────────────────────────────────────────────────────┤
│ Application SA: {project_name}-app                     │
│ Roles:                                                  │
│  • roles/aiplatform.user                               │
│  • roles/discoveryengine.editor                        │
│  • roles/logging.logWriter                             │
│  • roles/cloudtrace.agent                              │
│  • roles/storage.admin                                 │
│  • roles/secretmanager.secretAccessor (AlloyDB)        │
│                                                         │
│ Data Ingestion SA: {project_name}-rag                  │
│ Roles:                                                  │
│  • roles/storage.admin                                 │
│  • roles/aiplatform.user                               │
│  • roles/discoveryengine.admin                         │
│  • roles/logging.logWriter                             │
│  • roles/artifactregistry.writer                       │
│  • roles/bigquery.dataEditor                           │
│  • roles/bigquery.jobUser                              │
│  • roles/resourcemanager.projectIamAdmin               │
└─────────────────────────────────────────────────────────┘
```

### Role Assignment Patterns

#### 1. CI/CD Runner Project Roles

```hcl
# CI/CD runner has broad permissions in CICD project for building
resource "google_project_iam_member" "cicd_project_roles" {
  for_each = toset(var.cicd_roles)

  project = var.cicd_runner_project_id
  role    = each.value
  member  = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
}
```

**Default Roles:**
- `roles/run.invoker` - Can invoke Cloud Run services
- `roles/storage.admin` - Read/write storage
- `roles/aiplatform.user` - AI Platform access
- `roles/artifactregistry.writer` - Push container images
- `roles/cloudbuild.builds.builder` - Run Cloud Build jobs

#### 2. Deployment (Staging/Prod) Project Roles

```hcl
# CI/CD runner gets LIMITED permissions in Staging/Prod
resource "google_project_iam_member" "other_projects_roles" {
  for_each = {
    for pair in setproduct(keys(local.deploy_project_ids), var.cicd_sa_deployment_required_roles) :
    "${pair[0]}-${pair[1]}" => {
      project_id = local.deploy_project_ids[pair[0]]
      role       = pair[1]
    }
  }

  project = each.value.project_id
  role    = each.value.role
  member  = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
}
```

**Default Roles:**
- `roles/run.developer` - Deploy/update Cloud Run services
- `roles/iam.serviceAccountUser` - Impersonate app SA to run services
- `roles/aiplatform.user` - Model access
- `roles/storage.admin` - Storage access

#### 3. Application Service Account Roles

```hcl
# App SA gets permissions needed to RUN the agent
resource "google_project_iam_member" "app_sa_roles" {
  for_each = {
    for pair in setproduct(keys(local.deploy_project_ids), var.app_sa_roles) :
    join(",", pair) => {
      project = local.deploy_project_ids[pair[0]]
      role    = pair[1]
    }
  }

  project = each.value.project
  role    = each.value.role
  member  = "serviceAccount:${google_service_account.app_sa[split(",", each.key)[0]].email}"
}
```

**Default Roles:**
- `roles/aiplatform.user` - Call Gemini/Vertex AI APIs
- `roles/discoveryengine.editor` - Search/indexing access
- `roles/logging.logWriter` - Write application logs
- `roles/cloudtrace.agent` - Distributed tracing
- `roles/storage.admin` - Read/write data buckets
- `roles/secretmanager.secretAccessor` - Read secrets (AlloyDB)

#### 4. Cross-Project Container Registry Access

```hcl
# Allows Cloud Run in Staging/Prod to pull images from CICD repo
resource "google_project_iam_member" "cicd_run_invoker_artifact_registry_reader" {
  for_each = local.deploy_project_ids
  project  = var.cicd_runner_project_id

  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:service-${data.google_project.projects[each.key].number}@serverless-robot-prod.iam.gserviceaccount.com"
}
```

This uses the Cloud Run service agent to pull images.

#### 5. Service Account Impersonation

```hcl
# CI/CD SA can create service account tokens
resource "google_service_account_iam_member" "cicd_run_invoker_token_creator" {
  service_account_id = google_service_account.cicd_runner_sa.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
}

# CI/CD SA can use itself (for Cloud Build)
resource "google_service_account_iam_member" "cicd_run_invoker_account_user" {
  service_account_id = google_service_account.cicd_runner_sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
}
```

### IAM Best Practices Implemented

1. **Least Privilege:** Each SA has only necessary roles
2. **Separation of Concerns:**
   - CI/CD SA: Building and deployment
   - App SA: Runtime execution
   - Pipeline SA: Data processing
3. **Cross-Project Boundaries:** Different permissions per environment
4. **No Service Account Keys:** GitHub Actions uses WIF, Cloud Build uses ambient credentials
5. **Explicit Impersonation:** CI/CD SA explicitly impersonates app SA to run services

---

## Secret Management

### GCP Secret Manager Integration

Secrets are stored in Google Cloud Secret Manager and accessed by services during execution.

#### For GitHub Actions (WIF)

Secrets are automatically stored in GitHub as repository secrets:

```hcl
resource "github_actions_secret" "wif_pool_id" {
  repository      = var.repository_name
  secret_name     = "WIF_POOL_ID"
  plaintext_value = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
}

resource "github_actions_secret" "wif_provider_id" {
  repository      = var.repository_name
  secret_name     = "WIF_PROVIDER_ID"
  plaintext_value = google_iam_workload_identity_pool_provider.github_provider.workload_identity_pool_provider_id
}

resource "github_actions_secret" "gcp_service_account" {
  repository      = var.repository_name
  secret_name     = "GCP_SERVICE_ACCOUNT"
  plaintext_value = google_service_account.cicd_runner_sa.email
}
```

**Workflow Access:**
```yaml
- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/${{ env.GCP_PROJECT_NUMBER }}/locations/global/workloadIdentityPools/${{ secrets.WIF_POOL_ID }}/providers/${{ secrets.WIF_PROVIDER_ID }}
    service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}
```

#### For Cloud Build

GitHub PAT is stored in GCP Secret Manager:

```hcl
data "google_secret_manager_secret" "github_pat" {
  project   = var.cicd_runner_project_id
  secret_id = var.github_pat_secret_id  # Created via: gcloud secrets create github-pat --data-file=/dev/stdin
}

resource "google_secret_manager_secret_iam_member" "cloudbuild_secret_accessor" {
  project   = var.cicd_runner_project_id
  secret_id = data.google_secret_manager_secret.github_pat.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:service-${data.google_project.cicd_project.number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
}
```

**Cloud Build Usage:**
```yaml
availableSecrets:
  secretManager:
    - versionName: projects/$PROJECT_ID/secrets/github-pat/versions/latest
      env: 'GITHUB_PAT'
```

#### For Application Runtime Secrets

Applications use the application service account to access secrets:

```hcl
# AlloyDB password stored in Secret Manager
resource "google_secret_manager_secret" "db_password" {
  project   = var.dev_project_id
  secret_id = "${var.project_name}-db-password"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}

# Application can access via environment variable
resource "google_cloud_run_v2_service" "app" {
  template {
    containers {
      env {
        name = "DB_PASS"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_password.secret_id
            version = "latest"
          }
        }
      }
    }
  }
}
```

### Secret Rotation and Best Practices

1. **No Long-Lived Credentials:**
   - GitHub Actions: WIF tokens (~1 hour TTL)
   - Cloud Build: Service account credentials through IAM
   
2. **Automatic Secret Injection:**
   - GitHub Actions: `google-github-actions/auth` action
   - Cloud Build: `google-cloud-sdk` with service account

3. **Application Secrets:**
   - Stored in GCP Secret Manager
   - Accessed by application SA at runtime
   - Can be rotated without redeployment
   - Automatic versioning

---

## Staging to Production Promotion Workflow

### Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Developer Creates Pull Request                          │
│    (Pushes to feature branch)                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┴────────────────────┐
        │                                        │
        ▼                                        ▼
┌──────────────────────────────┐    ┌────────────────────────────┐
│ 2a. Cloud Build / GHA Triggers  │    │ 2b. PR Checks             │
│     PR Checks                   │    │  • Unit tests             │
└──────────────────────────────┘    │  • Linting (ruff, mypy)  │
                                    │  • Integration tests      │
                                    │  • E2E template tests     │
                                    └────────────────┬───────────┘
                                                     │
                                        ┌────────────┴────────────┐
                                        │                         │
                                    ✗ Fails               ✓ Passes
                                        │                         │
                                    Blocked                       ▼
                                    from merge    ┌──────────────────────────────┐
                                                  │ 3. Review and Merge          │
                                                  │ (Requires manual approval)   │
                                                  └────────────────┬─────────────┘
                                                                   │
                                    ┌──────────────────────────────┴────┐
                                    │                                    │
                                    ▼                                    ▼
                            ┌─────────────────────┐        ┌──────────────────────────┐
                            │ Merged to main      │        │ 4. Staging Build Trigger │
                            │ (Webhook event)     │        │ • Build Docker image     │
                            └────────────────────┬┘        │ • Push to Artifact Reg   │
                                                 │         │ • Deploy to staging      │
                                         ┌───────┘         └────────────┬─────────────┘
                                         │                             │
                                         ▼                             ▼
                                ┌──────────────────┐      ┌──────────────────────────┐
                                │ 5a. Staging      │      │ 5b. Staging Tests        │
                                │  • Load testing  │      │  • Smoke tests           │
                                │  • Validation    │      │  • Health checks         │
                                └────────────────┬─┘      └──────────────┬───────────┘
                                                 │                       │
                                    ┌────────────┴──────────────────────┴───┐
                                    │                                       │
                                ✓ Approved by manual gate              ✗ Failed
                                    │                                       │
                                    ▼                                       ▼
                            ┌─────────────────────┐              Staging blocked
                            │ 6. Prod Deployment  │              Retry needed
                            │ Trigger             │
                            │ • Same image        │
                            │ • Prod config       │
                            │ • Canary deploy     │
                            └────────────────────┘
                                    │
                                    ▼
                            ┌─────────────────────┐
                            │ 7. Production       │
                            │ Live Agent Service  │
                            └─────────────────────┘
```

### Stage 1: Pull Request Validation (Cloud Build)

**Cloud Build Triggers:**

```hcl
# PR Unit Tests
resource "google_cloudbuild_trigger" "pr_tests" {
  name            = "pr-tests"
  filename        = ".cloudbuild/ci/test.yaml"
  
  repository_event_config {
    repository = local.repository_path
    pull_request {
      branch          = "main"
      comment_control = "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"
    }
  }
}

# PR Linting
resource "google_cloudbuild_trigger" "pr_lint" {
  name            = "pr-lint"
  filename        = ".cloudbuild/ci/lint.yaml"
  
  repository_event_config {
    repository = local.repository_path
    pull_request {
      branch = "main"
    }
  }
}

# PR Template Agent Tests (for each agent/deployment combination)
resource "google_cloudbuild_trigger" "pr_templated_agents_test" {
  for_each = { for combo in local.agent_testing_combinations : combo.name => combo }

  name            = "test-${local.trigger_name_safe[each.key]}"
  filename        = ".cloudbuild/ci/test_templated_agents.yaml"
  
  repository_event_config {
    repository = local.repository_path
    pull_request {
      branch = "main"
    }
  }

  substitutions = {
    _TEST_AGENT_COMBINATION = each.value.value
  }
}
```

**Test Configuration (.cloudbuild/ci/test.yaml):**

```yaml
steps:
  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: install-dependencies
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        uv sync --dev --locked

  - name: "europe-west4-docker.pkg.dev/production-ai-template/starter-pack/e2e-tests"
    id: unit-tests
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        uv run pytest tests

logsBucket: gs://${PROJECT_ID}-logs-data/build-logs
options:
  defaultLogsBucketBehavior: REGIONAL_USER_OWNED_BUCKET
```

**Results:**
- All checks must pass before PR can be merged
- Status checks appear on PR
- Comments optional for external contributors

### Stage 2: Merge to Main → Staging Deployment

**Trigger Configuration (.github/workflows/staging.yaml for GitHub Actions):**

```yaml
name: Build and Deploy to Staging

on:
  push:
    branches:
      - main

permissions:
  contents: read
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://${{ env.STAGING_URL }}

    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/${{ env.GCP_PROJECT_NUMBER }}/locations/global/workloadIdentityPools/${{ secrets.WIF_POOL_ID }}/providers/${{ secrets.WIF_PROVIDER_ID }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Configure Docker authentication
        run: |
          gcloud auth configure-docker ${{ env.REGION }}-docker.pkg.dev

      - name: Build Docker image
        run: |
          docker build -t ${{ env.REGION }}-docker.pkg.dev/${{ env.CICD_PROJECT_ID }}/my-agent:${{ github.sha }} .

      - name: Push to Artifact Registry
        run: |
          docker push ${{ env.REGION }}-docker.pkg.dev/${{ env.CICD_PROJECT_ID }}/my-agent:${{ github.sha }}

      - name: Deploy to Cloud Run (Staging)
        run: |
          gcloud run deploy ${{ env.CONTAINER_NAME }} \
            --image ${{ env.REGION }}-docker.pkg.dev/${{ env.CICD_PROJECT_ID }}/my-agent:${{ github.sha }} \
            --platform managed \
            --region ${{ env.REGION }} \
            --project ${{ env.STAGING_PROJECT_ID }} \
            --service-account ${{ env.APP_SA_EMAIL_STAGING }}

      - name: Run staging tests
        run: |
          STAGING_URL=$(gcloud run services describe ${{ env.CONTAINER_NAME }} \
            --platform managed \
            --region ${{ env.REGION }} \
            --project ${{ env.STAGING_PROJECT_ID }} \
            --format 'value(status.url)')
          
          uv run pytest tests/integration/test_staging.py \
            --staging-url=$STAGING_URL
```

**Staging Deployment Process:**

1. **Image Build:**
   ```bash
   docker build -t us-central1-docker.pkg.dev/cicd-project/my-agent-repo/my-agent:abc123 .
   ```

2. **Push to Artifact Registry:**
   ```bash
   docker push us-central1-docker.pkg.dev/cicd-project/my-agent-repo/my-agent:abc123
   ```

3. **Deploy to Staging Cloud Run:**
   ```bash
   gcloud run deploy my-agent \
     --image us-central1-docker.pkg.dev/cicd-project/my-agent-repo/my-agent:abc123 \
     --platform managed \
     --region us-central1 \
     --project staging-project-id \
     --service-account my-agent-app@staging-project-id.iam.gserviceaccount.com
   ```

4. **Verify Deployment:**
   ```bash
   gcloud run services describe my-agent \
     --platform managed \
     --region us-central1 \
     --project staging-project-id
   ```

### Stage 3: Staging Validation and Testing

**Load Testing (Optional):**

```bash
# Simulated load test against staging environment
ab -n 1000 -c 50 https://my-agent-staging-abc123.run.app/

# Custom health checks
curl -X GET https://my-agent-staging-abc123.run.app/health
curl -X GET https://my-agent-staging-abc123.run.app/status
```

**Manual Approval Gate:**

The production deployment requires explicit approval:

```yaml
  deploy-to-prod:
    needs: build-and-deploy
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://${{ env.PROD_URL }}
    
    steps:
      # Approval is required before this job executes
      # Reviewers specified in environment protection rules
```

### Stage 4: Production Deployment

**Production Deployment Workflow (.github/workflows/deploy-to-prod.yaml):**

```yaml
name: Deploy to Production

on:
  workflow_run:
    workflows: ["Build and Deploy to Staging"]
    types:
      - completed
    branches:
      - main

permissions:
  contents: read
  id-token: write
  deployments: write

jobs:
  approve-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://${{ env.PROD_URL }}

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_commit }}

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/${{ env.GCP_PROJECT_NUMBER }}/locations/global/workloadIdentityPools/${{ secrets.WIF_POOL_ID }}/providers/${{ secrets.WIF_PROVIDER_ID }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Get image from staging build
        run: |
          # Retrieve the image URI from the staging deployment
          STAGING_IMAGE=$(gcloud run services describe ${{ env.CONTAINER_NAME }} \
            --platform managed \
            --region ${{ env.REGION }} \
            --project ${{ env.STAGING_PROJECT_ID }} \
            --format 'value(spec.template.spec.containers[0].image)')
          
          echo "PROD_IMAGE=$STAGING_IMAGE" >> $GITHUB_ENV

      - name: Deploy same image to Production
        run: |
          gcloud run deploy ${{ env.CONTAINER_NAME }} \
            --image ${{ env.PROD_IMAGE }} \
            --platform managed \
            --region ${{ env.REGION }} \
            --project ${{ env.PROD_PROJECT_ID }} \
            --service-account ${{ env.APP_SA_EMAIL_PROD }} \
            --no-traffic
          
          # Gradually shift traffic to new revision
          gcloud run services update-traffic ${{ env.CONTAINER_NAME }} \
            --to-revisions LATEST=100 \
            --platform managed \
            --region ${{ env.REGION }} \
            --project ${{ env.PROD_PROJECT_ID }}

      - name: Verify production deployment
        run: |
          PROD_URL=$(gcloud run services describe ${{ env.CONTAINER_NAME }} \
            --platform managed \
            --region ${{ env.REGION }} \
            --project ${{ env.PROD_PROJECT_ID }} \
            --format 'value(status.url)')
          
          # Health check
          curl --max-time 5 --retry 3 --retry-delay 2 \
            $PROD_URL/health

      - name: Create deployment
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.repos.createDeployment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: context.ref,
              environment: 'production',
              description: 'Deployed from staging'
            })
```

**Key Production Deployment Features:**

1. **Same Image from Staging:**
   - No rebuild in production
   - Exact same container tested in staging
   - Zero rebuild failures

2. **Blue-Green Deployment:**
   - New revision deployed with 0% traffic
   - Traffic shifted after verification
   - Instant rollback capability

3. **Gradual Rollout (Optional):**
   ```bash
   # Canary: 10% to new revision
   gcloud run services update-traffic my-agent \
     --to-revisions new-revision=10,old-revision=90

   # Monitor metrics for 5 minutes...

   # Full rollout: 100% to new revision
   gcloud run services update-traffic my-agent \
     --to-revisions new-revision=100
   ```

4. **Automatic Rollback:**
   ```bash
   # If errors detected
   gcloud run services update-traffic my-agent \
     --to-revisions old-revision=100
   ```

### Failure Handling

**PR Checks Failure:**
- Blocks merge to main
- Developer must fix and push new commit
- Checks re-run automatically

**Staging Deployment Failure:**
- Previous staging revision continues running
- Manual approval gate not triggered
- Developer gets notification
- Investigate in staging project logs

**Production Approval Denied:**
- Staging remains running unchanged
- Can retry approval after review
- Image remains in Artifact Registry

**Production Deployment Failure:**
- Previous production revision continues running
- Team notified immediately
- Quick rollback available:
  ```bash
  gcloud run services update-traffic my-agent \
    --to-revisions previous-revision=100
  ```

---

## Agent Engine Deployment Process

### Agent Engine Overview

Agent Engine is Google Cloud's serverless execution environment optimized for AI agents.

**Key Differences from Cloud Run:**
- Agent-specific runtime
- Better AI integration
- Different scaling model
- No container image required (YAML-based)

### Agent Engine Terraform Configuration

**Base Template (base_template/deployment/terraform/):**

The Terraform configuration for Agent Engine is conditional based on the deployment target selected during agent creation.

```hcl
{% if cookiecutter.deployment_target == 'agent_engine' %}
# Agent Engine specific configuration
resource "google_vertex_ai_agent" "app_agent" {
  for_each = local.deploy_project_ids

  display_name = var.project_name
  location     = var.region
  project      = each.value
  
  agent_config {
    agent_type = "AGENT_ENGINE"
  }

  service_account = google_service_account.app_sa[each.key].email
}
{% endif %}
```

### Deployment Process

**1. Build Phase (Not applicable for Agent Engine):**
- Agent Engine uses YAML-based agents
- No Docker container needed
- No Artifact Registry push

**2. Deploy Phase:**

```bash
# Terraform deployment creates Agent Engine resource
terraform apply \
  -var-file="deployment/terraform/vars/env.tfvars" \
  -var="prod_project_id=your-prod-project" \
  -var="staging_project_id=your-staging-project"
```

**3. Execute Agent:**

```python
from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(
    project="your-project",
    location="us-central1"
)

# Get agent
agent = aiplatform.Agent(resource_name="your-agent-resource-name")

# Execute agent
response = agent.send_message(
    input_text="User query here"
)
print(response.text)
```

### Agent Engine IAM Configuration

The Agent Engine service requires specific IAM permissions:

```hcl
# Vertex AI Service Account permissions (automatic service agent)
resource "google_project_iam_member" "vertex_ai_sa_permissions" {
  for_each = {
    for pair in setproduct(keys(local.project_ids), var.app_sa_roles) :
    join(",", pair) => pair[1]
  }

  project = var.dev_project_id
  role    = each.value
  member  = google_project_service_identity.vertex_sa.member
}

# Get service identity for Vertex AI
resource "google_project_service_identity" "vertex_sa" {
  provider = google-beta
  project  = var.dev_project_id
  service  = "aiplatform.googleapis.com"
}
```

### Accessing Agent Engine

**Via Python SDK:**

```python
from google.cloud import aiplatform
from google.api_core import gapic_v1

# Create client
client = aiplatform.gapic.v1.AgentServiceClient(
    credentials=service_account.Credentials.from_service_account_file(
        'service-account-key.json'
    )
)

# Prepare request
request = aiplatform.gapic.v1.ExecuteAgentRequest(
    name="projects/PROJECT/locations/REGION/agents/AGENT_ID",
    input_text="Your query"
)

# Execute
response = client.execute_agent(request=request)
```

**Via REST API:**

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"inputText": "Your query"}' \
  https://aiplatform.googleapis.com/v1/projects/PROJECT/locations/REGION/agents/AGENT_ID:execute
```

---

## Cloud Run Deployment Process

### Cloud Run Overview

Cloud Run provides container-based serverless deployment with full control over the container image.

### Docker Image Build and Push

**Dockerfile Example:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY agent_starter_pack/ ./agent_starter_pack/

# Install dependencies
RUN pip install --no-cache-dir uv
RUN uv sync --frozen --no-dev

# Set service account and run entrypoint
ENTRYPOINT ["uv", "run", "python", "-m", "agent_starter_pack.agents.my_agent.app"]
```

**Build and Push Script:**

```bash
#!/bin/bash
set -e

PROJECT_ID=$1
REGION=${2:-us-central1}
IMAGE_NAME=$3

# Build image
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-agent-repo/${IMAGE_NAME}:latest .

# Push to Artifact Registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-agent-repo/${IMAGE_NAME}:latest

echo "Image pushed: ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-agent-repo/${IMAGE_NAME}:latest"
```

### Cloud Run Service Terraform Configuration

**Dev Environment (cloud_run/deployment/terraform/dev/service.tf):**

```hcl
resource "google_cloud_run_v2_service" "app" {
  name                = var.project_name
  location            = var.region
  project             = var.dev_project_id
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"  # Placeholder

      resources {
        limits = {
          cpu    = "4"
          memory = "8Gi"
        }
      }

      # Environment variables
      {% if data_ingestion %}
      env {
        name  = "DATA_STORE_ID"
        value = google_discovery_engine_data_store.data_store_dev.data_store_id
      }

      env {
        name  = "VECTOR_SEARCH_INDEX"
        value = google_vertex_ai_index.vector_search_index.id
      }
      {% endif %}

      # Secret injection
      {% if is_adk and session_type == "alloydb" %}
      env {
        name  = "DB_HOST"
        value = google_alloydb_instance.session_db_instance.ip_address
      }

      env {
        name = "DB_PASS"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_password.secret_id
            version = "latest"
          }
        }
      }
      {% endif %}
    }

    service_account = google_service_account.app_sa.email
    max_instance_request_concurrency = 40

    scaling {
      min_instance_count = 1
      max_instance_count = 10
    }

    session_affinity = true

    # VPC access for AlloyDB
    {% if is_adk and session_type == "alloydb" %}
    vpc_access {
      network_interfaces {
        network    = google_compute_network.default.id
        subnetwork = google_compute_subnetwork.default.id
      }
    }
    {% endif %}
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  # Allow CI/CD to update image without Terraform conflicts
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }
}
```

**Key Configuration Details:**

1. **Image Placeholder:**
   - Initial image is just a placeholder (`hello` image)
   - CI/CD pipeline updates to actual image on deployment
   - `ignore_changes` prevents Terraform from reverting

2. **CPU/Memory:**
   ```hcl
   resources {
     limits = {
       cpu    = "4"
       memory = "8Gi"
     }
   }
   ```
   Cloud Run pricing is per CPU-second, so appropriate sizing is important

3. **Scaling Configuration:**
   ```hcl
   scaling {
     min_instance_count = 1  # Always 1 instance ready
     max_instance_count = 10  # Scale up to 10 instances
   }
   ```

4. **Concurrency:**
   ```hcl
   max_instance_request_concurrency = 40  # Max 40 requests per instance
   ```

5. **Session Affinity:**
   ```hcl
   session_affinity = true  # Sticky sessions for stateful apps
   ```

### Cloud Run Deployment via CI/CD

**GitHub Actions Workflow:**

```yaml
- name: Deploy to Cloud Run (Staging)
  run: |
    gcloud run deploy my-agent \
      --image us-central1-docker.pkg.dev/${{ env.CICD_PROJECT_ID }}/my-agent-repo/my-agent:${{ github.sha }} \
      --platform managed \
      --region us-central1 \
      --project ${{ env.STAGING_PROJECT_ID }} \
      --service-account my-agent-app@${{ env.STAGING_PROJECT_ID }}.iam.gserviceaccount.com \
      --no-traffic  # Don't immediately route traffic

- name: Verify Staging Deployment
  run: |
    # Get the service URL
    STAGING_URL=$(gcloud run services describe my-agent \
      --platform managed \
      --region us-central1 \
      --project ${{ env.STAGING_PROJECT_ID }} \
      --format 'value(status.url)')
    
    # Health check
    curl --max-time 5 --retry 3 $STAGING_URL/health
```

**Cloud Build Configuration (.cloudbuild/staging.yaml):**

```yaml
steps:
  # Build step
  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-image'
    args:
      - 'build'
      - '-t'
      - '${REGION}-docker.pkg.dev/${PROJECT_ID}/my-agent-repo/my-agent:latest'
      - '-t'
      - '${REGION}-docker.pkg.dev/${PROJECT_ID}/my-agent-repo/my-agent:${COMMIT_SHA}'
      - '.'

  # Push step
  - name: 'gcr.io/cloud-builders/docker'
    id: 'push-image'
    args:
      - 'push'
      - '${REGION}-docker.pkg.dev/${PROJECT_ID}/my-agent-repo/my-agent:${COMMIT_SHA}'

  # Deploy step
  - name: 'gcr.io/cloud-builders/gke-deploy'
    id: 'deploy-staging'
    args:
      - 'run'
      - '--platform'
      - 'managed'
      - '--region'
      - '${REGION}'
      - '--project'
      - '${STAGING_PROJECT_ID}'

images:
  - '${REGION}-docker.pkg.dev/${PROJECT_ID}/my-agent-repo/my-agent:${COMMIT_SHA}'

substitutions:
  _REGION: 'us-central1'
  _STAGING_PROJECT_ID: 'your-staging-project'
```

### Cloud Run Traffic Management

**Blue-Green Deployment:**

```bash
# Deploy new revision with 0% traffic
gcloud run deploy my-agent \
  --image new-image:latest \
  --no-traffic \
  --platform managed \
  --region us-central1 \
  --project prod-project

# Verify new revision
gcloud run revisions describe my-agent-new-revision \
  --platform managed \
  --region us-central1 \
  --project prod-project

# Shift traffic after verification
gcloud run services update-traffic my-agent \
  --to-revisions new-revision=100
```

**Canary Deployment (Gradual Rollout):**

```bash
# Shift 10% traffic to new revision
gcloud run services update-traffic my-agent \
  --to-revisions new-revision=10,old-revision=90

# Monitor error rates and latency...

# Increase to 25%
gcloud run services update-traffic my-agent \
  --to-revisions new-revision=25,old-revision=75

# Full rollout
gcloud run services update-traffic my-agent \
  --to-revisions new-revision=100
```

**Quick Rollback:**

```bash
# Immediately revert to previous revision
gcloud run services update-traffic my-agent \
  --to-revisions old-revision=100
```

### Monitoring Cloud Run Deployments

```bash
# View service status
gcloud run services describe my-agent \
  --platform managed \
  --region us-central1 \
  --project prod-project

# View recent revisions
gcloud run revisions list \
  --service my-agent \
  --platform managed \
  --region us-central1 \
  --project prod-project

# View logs
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=my-agent" \
  --limit 100 \
  --format json \
  --project prod-project

# View metrics
gcloud monitoring time-series list \
  --filter 'resource.type = "cloud_run_revision"' \
  --format json
```

---

## Deployment Commands and Automation

### Manual Deployment Commands

#### 1. Initialize Development Environment

```bash
# Set GCP project
gcloud config set project your-dev-project-id

# Deploy development infrastructure
terraform -chdir=deployment/terraform/dev apply \
  -var-file="vars/env.tfvars" \
  -var="dev_project_id=your-dev-project-id" \
  -var="region=us-central1"

# Create Cloud Run service
gcloud run deploy my-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --project your-dev-project-id \
  --service-account my-agent-app@your-dev-project-id.iam.gserviceaccount.com
```

#### 2. Setup CI/CD Pipeline (Automated via CLI)

```bash
# From project root:
uvx agent-starter-pack setup-cicd \
  --staging-project your-staging-project-id \
  --prod-project your-prod-project-id \
  --repository-name my-awesome-agent \
  --repository-owner my-org-name
```

The `setup-cicd` command automatically:
1. Configures Terraform variables
2. Runs `terraform apply` for infrastructure
3. Creates GitHub Actions or Cloud Build triggers
4. Initializes local Git repository
5. Sets up remote state (GCS bucket)

**Manual Alternative (step-by-step):**

```bash
# 1. Create variables file
cat > deployment/terraform/vars/env.tfvars << EOF
project_name       = "my-agent"
prod_project_id    = "your-prod-project-id"
staging_project_id = "your-staging-project-id"
cicd_runner_project_id = "your-cicd-project-id"
region             = "us-central1"
repository_owner   = "your-github-org"
repository_name    = "my-awesome-agent"
