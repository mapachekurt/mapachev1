terraform {
  backend "gcs" {
    bucket = "my-agent-terraform-state-12345"
    prefix = "prod"
  }
}
