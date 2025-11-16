# Variables for SaaS Agent Terraform module

variable "agent_name" {
  description = "Name of the SaaS agent (snake_case)"
  type        = string
}

variable "agent_id" {
  description = "Unique agent ID (e.g., agent_512)"
  type        = string
}

variable "display_name" {
  description = "Human-readable display name"
  type        = string
}

variable "tier" {
  description = "Agent tier classification"
  type        = string
  validation {
    condition     = contains(["tier_1", "tier_2", "tier_3", "tier_4", "tier_5"], var.tier)
    error_message = "Tier must be one of: tier_1, tier_2, tier_3, tier_4, tier_5"
  }
}

variable "category" {
  description = "Agent category (e.g., communication, crm, analytics)"
  type        = string
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for deployment"
  type        = string
  default     = "us-central1"
}

variable "model" {
  description = "AI model to use for the agent"
  type        = string
  default     = "gemini-2.0-flash-exp"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod"
  }
}

variable "notification_channels" {
  description = "List of notification channel IDs for alerts"
  type        = list(string)
  default     = []
}

variable "enable_monitoring" {
  description = "Enable monitoring and alerting"
  type        = bool
  default     = true
}

variable "enable_logging" {
  description = "Enable structured logging"
  type        = bool
  default     = true
}

variable "cpu_limit" {
  description = "CPU limit for the agent container"
  type        = string
  default     = "2000m"
}

variable "memory_limit" {
  description = "Memory limit for the agent container"
  type        = string
  default     = "4Gi"
}

variable "min_instances" {
  description = "Minimum number of instances"
  type        = number
  default     = 0
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 10
}

variable "timeout_seconds" {
  description = "Request timeout in seconds"
  type        = number
  default     = 300
}

variable "labels" {
  description = "Additional labels to apply to resources"
  type        = map(string)
  default     = {}
}
