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

# Monitoring and alerting configuration for multi-agent system

# Variables for notification channels
variable "alert_email" {
  description = "Email address for alert notifications"
  type        = string
  default     = ""
}

variable "enable_alerts" {
  description = "Enable monitoring alerts (set to false for dev environments)"
  type        = bool
  default     = true
}

# Notification channels for alerts
resource "google_monitoring_notification_channel" "email" {
  for_each = var.alert_email != "" && var.enable_alerts ? local.deploy_project_ids : {}

  project      = each.value
  display_name = "Email Notifications"
  type         = "email"

  labels = {
    email_address = var.alert_email
  }

  depends_on = [google_project_service.deploy_project_services]
}

# Alert Policy: High Error Rate
resource "google_monitoring_alert_policy" "high_error_rate" {
  for_each = var.enable_alerts ? local.deploy_project_ids : {}

  project      = each.value
  display_name = "${var.project_name} - High Error Rate (${each.key})"
  combiner     = "OR"

  documentation {
    content   = <<-EOT
      ## High Error Rate Alert

      This alert triggers when the Cloud Run service error rate exceeds 5% over a 5-minute window.

      **Environment:** ${each.key}

      **Troubleshooting Steps:**
      1. Check Cloud Run logs: `gcloud logging read "resource.type=cloud_run_revision" --project=${each.value} --limit=50`
      2. Review error traces in Cloud Trace
      3. Check BigQuery telemetry dataset for error patterns
      4. Review recent deployments for potential issues
      5. Verify all dependencies (Vertex AI, Discovery Engine) are healthy

      **Escalation:** If errors persist > 15 minutes, page on-call engineer
    EOT
    mime_type = "text/markdown"
  }

  conditions {
    display_name = "Error rate > 5%"

    condition_threshold {
      filter          = <<-EOT
        resource.type = "cloud_run_revision"
        AND resource.labels.service_name = "${var.project_name}"
        AND metric.type = "run.googleapis.com/request_count"
        AND metric.labels.response_code_class = "5xx"
      EOT

      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.05

      aggregations {
        alignment_period     = "60s"
        per_series_aligner   = "ALIGN_RATE"
        cross_series_reducer = "REDUCE_SUM"
        group_by_fields      = ["resource.service_name"]
      }

      trigger {
        count = 1
      }
    }
  }

  notification_channels = var.alert_email != "" ? [google_monitoring_notification_channel.email[each.key].id] : []

  alert_strategy {
    auto_close = "86400s" # 24 hours

    notification_rate_limit {
      period = "300s" # Don't send more than 1 notification per 5 minutes
    }
  }

  depends_on = [google_project_service.deploy_project_services]
}

# Alert Policy: High Latency (P99 > 10 seconds)
resource "google_monitoring_alert_policy" "high_latency" {
  for_each = var.enable_alerts ? local.deploy_project_ids : {}

  project      = each.value
  display_name = "${var.project_name} - High P99 Latency (${each.key})"
  combiner     = "OR"

  documentation {
    content   = <<-EOT
      ## High Latency Alert

      This alert triggers when P99 request latency exceeds 10 seconds over a 5-minute window.

      **Environment:** ${each.key}

      **Troubleshooting Steps:**
      1. Check agent performance metrics in BigQuery analytics dataset
      2. Review Cloud Trace for slow operations
      3. Check if specific agents or tools are causing slowdowns
      4. Verify Vertex AI API quotas and latency
      5. Check for token count spikes (large prompts/responses)
      6. Review Cloud Run instance counts and scaling behavior

      **Optimization Actions:**
      - Consider increasing Cloud Run instance concurrency
      - Optimize agent prompts for shorter responses
      - Implement caching for repeated queries
      - Review and optimize tool execution logic
    EOT
    mime_type = "text/markdown"
  }

  conditions {
    display_name = "P99 latency > 10 seconds"

    condition_threshold {
      filter          = <<-EOT
        resource.type = "cloud_run_revision"
        AND resource.labels.service_name = "${var.project_name}"
        AND metric.type = "run.googleapis.com/request_latencies"
      EOT

      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 10000 # milliseconds

      aggregations {
        alignment_period     = "60s"
        per_series_aligner   = "ALIGN_DELTA"
        cross_series_reducer = "REDUCE_PERCENTILE_99"
        group_by_fields      = ["resource.service_name"]
      }

      trigger {
        count = 1
      }
    }
  }

  notification_channels = var.alert_email != "" ? [google_monitoring_notification_channel.email[each.key].id] : []

  alert_strategy {
    auto_close = "86400s"

    notification_rate_limit {
      period = "300s"
    }
  }

  depends_on = [google_project_service.deploy_project_services]
}

# Alert Policy: High Daily Cost (Production only)
resource "google_monitoring_alert_policy" "high_daily_cost" {
  for_each = var.enable_alerts && each.key == "prod" ? { prod = local.deploy_project_ids.prod } : {}

  project      = each.value
  display_name = "${var.project_name} - High Daily Cost Alert"
  combiner     = "OR"

  documentation {
    content   = <<-EOT
      ## High Daily Cost Alert

      This alert triggers when estimated daily LLM costs exceed $100.

      **Troubleshooting Steps:**
      1. Query cost analysis view in BigQuery:
         ```sql
         SELECT * FROM `${each.value}.${var.project_name}_analytics.cost_analysis`
         WHERE date = CURRENT_DATE()
         ORDER BY estimated_cost_usd DESC
         ```
      2. Identify which agents/models are generating high costs
      3. Check for unexpected traffic spikes
      4. Review token usage patterns
      5. Check for infinite loops or error retry storms

      **Optimization Actions:**
      - Switch high-volume agents to Gemini 2.0 Flash (cheaper)
      - Implement response caching
      - Optimize prompts to reduce output tokens
      - Set max_tokens limits on agent configurations
      - Implement rate limiting for expensive operations
    EOT
    mime_type = "text/markdown"
  }

  conditions {
    display_name = "Daily LLM cost > $100"

    condition_threshold {
      filter          = <<-EOT
        resource.type = "global"
        AND metric.type = "logging.googleapis.com/user/estimated_daily_cost"
      EOT

      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 100

      aggregations {
        alignment_period   = "3600s" # 1 hour
        per_series_aligner = "ALIGN_MAX"
      }

      trigger {
        count = 1
      }
    }
  }

  notification_channels = var.alert_email != "" ? [google_monitoring_notification_channel.email[each.key].id] : []

  alert_strategy {
    auto_close = "86400s"

    notification_rate_limit {
      period = "3600s" # Max 1 notification per hour for cost alerts
    }
  }

  depends_on = [google_project_service.deploy_project_services]
}

# Alert Policy: Low Request Rate (might indicate service down)
resource "google_monitoring_alert_policy" "low_request_rate" {
  for_each = var.enable_alerts && each.key == "prod" ? { prod = local.deploy_project_ids.prod } : {}

  project      = each.value
  display_name = "${var.project_name} - Low Request Rate (${each.key})"
  combiner     = "OR"

  documentation {
    content   = <<-EOT
      ## Low Request Rate Alert

      This alert triggers when request rate drops below expected baseline, potentially indicating service issues.

      **Environment:** ${each.key}

      **Troubleshooting Steps:**
      1. Check if service is running: `gcloud run services describe ${var.project_name} --project=${each.value}`
      2. Verify no recent failed deployments
      3. Check for upstream service issues (API gateway, load balancer)
      4. Review Cloud Run logs for cold start issues
      5. Verify service is not accidentally set to no-traffic
    EOT
    mime_type = "text/markdown"
  }

  conditions {
    display_name = "Request rate dropped significantly"

    condition_threshold {
      filter          = <<-EOT
        resource.type = "cloud_run_revision"
        AND resource.labels.service_name = "${var.project_name}"
        AND metric.type = "run.googleapis.com/request_count"
      EOT

      duration        = "600s"
      comparison      = "COMPARISON_LT"
      threshold_value = 1 # Less than 1 request per minute for 10 minutes

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }

      trigger {
        count = 1
      }
    }
  }

  notification_channels = var.alert_email != "" ? [google_monitoring_notification_channel.email[each.key].id] : []

  alert_strategy {
    auto_close = "3600s"

    notification_rate_limit {
      period = "600s"
    }
  }

  depends_on = [google_project_service.deploy_project_services]
}

# Alert Policy: Cloud Run Instance Scaling Issues
resource "google_monitoring_alert_policy" "instance_scaling" {
  for_each = var.enable_alerts ? local.deploy_project_ids : {}

  project      = each.value
  display_name = "${var.project_name} - Instance Scaling Issues (${each.key})"
  combiner     = "OR"

  documentation {
    content   = <<-EOT
      ## Instance Scaling Issues

      This alert triggers when Cloud Run instances are maxed out, indicating scaling limits reached.

      **Environment:** ${each.key}

      **Actions:**
      1. Review current instance count vs. maximum
      2. Check if max_instances limit needs to be increased
      3. Verify requests are being load balanced correctly
      4. Consider increasing instance concurrency if CPU/memory allows
      5. Check for quota limits on Cloud Run instances
    EOT
    mime_type = "text/markdown"
  }

  conditions {
    display_name = "Instance count at maximum"

    condition_threshold {
      filter          = <<-EOT
        resource.type = "cloud_run_revision"
        AND resource.labels.service_name = "${var.project_name}"
        AND metric.type = "run.googleapis.com/container/instance_count"
      EOT

      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = each.key == "prod" ? 80 : 8 # 80% of prod max (100), 80% of staging max (10)

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MAX"
      }

      trigger {
        count = 1
      }
    }
  }

  notification_channels = var.alert_email != "" ? [google_monitoring_notification_channel.email[each.key].id] : []

  alert_strategy {
    auto_close = "3600s"

    notification_rate_limit {
      period = "900s"
    }
  }

  depends_on = [google_project_service.deploy_project_services]
}

# Uptime check for production service
resource "google_monitoring_uptime_check_config" "https_uptime_check" {
  for_each = each.key == "prod" ? { prod = local.deploy_project_ids.prod } : {}

  project      = each.value
  display_name = "${var.project_name} Production Health Check"
  timeout      = "10s"
  period       = "60s"

  http_check {
    path         = "/health"
    port         = 443
    use_ssl      = true
    validate_ssl = true
  }

  monitored_resource {
    type = "uptime_url"
    labels = {
      project_id = each.value
      host       = "${var.project_name}-${substr(md5(each.value), 0, 8)}.${var.region}.run.app"
    }
  }

  depends_on = [google_project_service.deploy_project_services]
}

# Dashboard for agent metrics
resource "google_monitoring_dashboard" "agent_dashboard" {
  for_each = local.deploy_project_ids

  project        = each.value
  dashboard_json = jsonencode({
    displayName = "${var.project_name} Agent Metrics - ${each.key}"
    mosaicLayout = {
      columns = 12
      tiles = [
        {
          width  = 6
          height = 4
          widget = {
            title = "Request Rate"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.project_name}\" metric.type=\"run.googleapis.com/request_count\""
                    aggregation = {
                      alignmentPeriod  = "60s"
                      perSeriesAligner = "ALIGN_RATE"
                    }
                  }
                }
              }]
            }
          }
        },
        {
          xPos   = 6
          width  = 6
          height = 4
          widget = {
            title = "Error Rate"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.project_name}\" metric.type=\"run.googleapis.com/request_count\" metric.labels.response_code_class=\"5xx\""
                    aggregation = {
                      alignmentPeriod  = "60s"
                      perSeriesAligner = "ALIGN_RATE"
                    }
                  }
                }
              }]
            }
          }
        },
        {
          yPos   = 4
          width  = 6
          height = 4
          widget = {
            title = "P50/P95/P99 Latency"
            xyChart = {
              dataSets = [
                {
                  timeSeriesQuery = {
                    timeSeriesFilter = {
                      filter = "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.project_name}\" metric.type=\"run.googleapis.com/request_latencies\""
                      aggregation = {
                        alignmentPeriod    = "60s"
                        perSeriesAligner   = "ALIGN_DELTA"
                        crossSeriesReducer = "REDUCE_PERCENTILE_50"
                      }
                    }
                  }
                  plotType = "LINE"
                },
                {
                  timeSeriesQuery = {
                    timeSeriesFilter = {
                      filter = "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.project_name}\" metric.type=\"run.googleapis.com/request_latencies\""
                      aggregation = {
                        alignmentPeriod    = "60s"
                        perSeriesAligner   = "ALIGN_DELTA"
                        crossSeriesReducer = "REDUCE_PERCENTILE_95"
                      }
                    }
                  }
                  plotType = "LINE"
                },
                {
                  timeSeriesQuery = {
                    timeSeriesFilter = {
                      filter = "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.project_name}\" metric.type=\"run.googleapis.com/request_latencies\""
                      aggregation = {
                        alignmentPeriod    = "60s"
                        perSeriesAligner   = "ALIGN_DELTA"
                        crossSeriesReducer = "REDUCE_PERCENTILE_99"
                      }
                    }
                  }
                  plotType = "LINE"
                }
              ]
            }
          }
        },
        {
          xPos   = 6
          yPos   = 4
          width  = 6
          height = 4
          widget = {
            title = "Instance Count"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.project_name}\" metric.type=\"run.googleapis.com/container/instance_count\""
                    aggregation = {
                      alignmentPeriod  = "60s"
                      perSeriesAligner = "ALIGN_MAX"
                    }
                  }
                }
              }]
            }
          }
        }
      ]
    }
  })

  depends_on = [google_project_service.deploy_project_services]
}
