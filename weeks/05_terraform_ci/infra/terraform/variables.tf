variable "environment" {
  type        = string
  description = "dev, test or prod"
  default     = "dev"
}

variable "lake_name" {
  type        = string
  description = "Base name of the data lake"
  default     = "retail-lake"
}

variable "spark_version" {
  type    = string
  default = "14.3.x-scala2.12"
}

variable "node_type_id" {
  type        = string
  description = "Cloud-specific VM size; set per cloud provider"
  default     = "Standard_DS3_v2"
}
