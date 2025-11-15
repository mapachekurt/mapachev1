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

# BigQuery datasets for analytics and trace analysis
# Note: Log sink datasets are in log_sinks.tf

# Analytics dataset for custom agent metrics and analysis
resource "google_bigquery_dataset" "analytics" {
  for_each = local.deploy_project_ids

  project       = each.value
  dataset_id    = replace("${var.project_name}_analytics", "-", "_")
  friendly_name = "${var.project_name} Analytics"
  description   = "Dataset for agent performance analytics, cost analysis, and custom metrics"
  location      = var.region

  # Data retention: 90 days for cost optimization
  default_partition_expiration_ms = 7776000000 # 90 days

  # Table expiration: Tables without partitioning expire after 90 days
  default_table_expiration_ms = 7776000000

  labels = {
    environment = each.key
    purpose     = "analytics"
    managed_by  = "terraform"
  }

  depends_on = [resource.google_project_service.deploy_project_services]
}

# Dataset for agent evaluation results from Vertex AI
resource "google_bigquery_dataset" "evaluations" {
  for_each = local.deploy_project_ids

  project       = each.value
  dataset_id    = replace("${var.project_name}_evaluations", "-", "_")
  friendly_name = "${var.project_name} Evaluations"
  description   = "Dataset for storing agent evaluation results from Vertex AI and custom evaluations"
  location      = var.region

  # Longer retention for evaluation results (180 days)
  default_partition_expiration_ms = 15552000000 # 180 days

  labels = {
    environment = each.key
    purpose     = "evaluations"
    managed_by  = "terraform"
  }

  depends_on = [resource.google_project_service.deploy_project_services]
}

# Create view in analytics dataset for agent performance metrics
resource "google_bigquery_table" "agent_performance_view" {
  for_each = local.deploy_project_ids

  project    = each.value
  dataset_id = google_bigquery_dataset.analytics[each.key].dataset_id
  table_id   = "agent_performance"

  view {
    query = <<-SQL
      SELECT
        TIMESTAMP_TRUNC(timestamp, HOUR) as hour,
        JSON_EXTRACT_SCALAR(jsonPayload, '$.agent_name') as agent_name,
        JSON_EXTRACT_SCALAR(jsonPayload, '$.model') as model,
        COUNT(*) as invocation_count,
        AVG(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.latency_ms') AS FLOAT64)) as avg_latency_ms,
        MAX(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.latency_ms') AS FLOAT64)) as max_latency_ms,
        APPROX_QUANTILES(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.latency_ms') AS FLOAT64), 100)[OFFSET(99)] as p99_latency_ms,
        COUNTIF(JSON_EXTRACT_SCALAR(jsonPayload, '$.error') IS NOT NULL) as error_count,
        SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.input_tokens') AS INT64)) as total_input_tokens,
        SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.output_tokens') AS INT64)) as total_output_tokens
      FROM `${each.value}.${google_bigquery_dataset.telemetry_logs_dataset[each.key].dataset_id}.*`
      WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
      GROUP BY hour, agent_name, model
      ORDER BY hour DESC, invocation_count DESC
    SQL

    use_legacy_sql = false
  }

  depends_on = [google_bigquery_dataset.analytics, google_bigquery_dataset.telemetry_logs_dataset]
}

# Create view for cost analysis
resource "google_bigquery_table" "cost_analysis_view" {
  for_each = local.deploy_project_ids

  project    = each.value
  dataset_id = google_bigquery_dataset.analytics[each.key].dataset_id
  table_id   = "cost_analysis"

  view {
    query = <<-SQL
      SELECT
        DATE(timestamp) as date,
        JSON_EXTRACT_SCALAR(jsonPayload, '$.model') as model,
        JSON_EXTRACT_SCALAR(jsonPayload, '$.agent_name') as agent_name,
        SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.input_tokens') AS INT64)) as total_input_tokens,
        SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.output_tokens') AS INT64)) as total_output_tokens,
        -- Gemini 2.0 Flash pricing: $0.075 per 1M input tokens, $0.30 per 1M output tokens
        -- Gemini 1.5 Pro pricing: $1.25 per 1M input tokens, $5.00 per 1M output tokens
        CASE JSON_EXTRACT_SCALAR(jsonPayload, '$.model')
          WHEN 'gemini-2.0-flash-exp' THEN
            (SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.input_tokens') AS INT64)) * 0.075 / 1000000) +
            (SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.output_tokens') AS INT64)) * 0.30 / 1000000)
          WHEN 'gemini-1.5-pro' THEN
            (SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.input_tokens') AS INT64)) * 1.25 / 1000000) +
            (SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.output_tokens') AS INT64)) * 5.00 / 1000000)
          ELSE
            (SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.input_tokens') AS INT64)) * 0.075 / 1000000) +
            (SUM(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.output_tokens') AS INT64)) * 0.30 / 1000000)
        END as estimated_cost_usd
      FROM `${each.value}.${google_bigquery_dataset.telemetry_logs_dataset[each.key].dataset_id}.*`
      WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
      GROUP BY date, model, agent_name
      ORDER BY date DESC, estimated_cost_usd DESC
    SQL

    use_legacy_sql = false
  }

  depends_on = [google_bigquery_dataset.analytics, google_bigquery_dataset.telemetry_logs_dataset]
}

# Grant BigQuery User role to application service accounts
resource "google_project_iam_member" "app_sa_bigquery_user" {
  for_each = local.deploy_project_ids

  project = each.value
  role    = "roles/bigquery.user"
  member  = "serviceAccount:${google_service_account.app_sa[each.key].email}"

  depends_on = [google_service_account.app_sa]
}

# Grant BigQuery Data Editor role for analytics dataset
resource "google_bigquery_dataset_iam_member" "app_sa_analytics_editor" {
  for_each = local.deploy_project_ids

  project    = each.value
  dataset_id = google_bigquery_dataset.analytics[each.key].dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.app_sa[each.key].email}"

  depends_on = [google_bigquery_dataset.analytics, google_service_account.app_sa]
}

# Grant BigQuery Data Editor role for evaluations dataset
resource "google_bigquery_dataset_iam_member" "app_sa_evaluations_editor" {
  for_each = local.deploy_project_ids

  project    = each.value
  dataset_id = google_bigquery_dataset.evaluations[each.key].dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.app_sa[each.key].email}"

  depends_on = [google_bigquery_dataset.evaluations, google_service_account.app_sa]
}
