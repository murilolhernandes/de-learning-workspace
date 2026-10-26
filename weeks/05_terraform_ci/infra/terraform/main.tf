# Learning example only. Never applied. Validate/plan only.
terraform {
  required_version = ">= 1.5"
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.40"
    }
  }
}

# Generic storage bucket, shown with the "local" provider so it needs no cloud account.
resource "local_file" "lake_marker" {
  filename = "${path.module}/.lake/${var.environment}/README.txt"
  content  = "Placeholder for the ${var.environment} data lake bucket (${var.lake_name})."
}

# Databricks workspace-level resource: a small job cluster definition.
# Provider auth comes from environment variables at run time. Do not put credentials in .tf files.
resource "databricks_cluster" "etl" {
  cluster_name            = "${var.lake_name}-${var.environment}-etl"
  spark_version           = var.spark_version
  node_type_id            = var.node_type_id
  autotermination_minutes = 20
  num_workers             = 1
}
