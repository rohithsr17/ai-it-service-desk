variable "aws_region" {
  type = string
}

variable "ticket_table_name" {
  type    = string
  default = "itsm-demo-tickets"
}

variable "lambda_function_name" {
  type    = string
  default = "itsm-lex-handler"
}

variable "lambda_zip_path" {
  type    = string
  default = "lambda.zip"
}

variable "lambda_timeout_seconds" {
  type    = number
  default = 15
}

variable "lambda_memory_mb" {
  type    = number
  default = 512
}

variable "bedrock_enabled" {
  type    = bool
  default = false
}

variable "bedrock_model_id" {
  type    = string
  default = ""
}

variable "bedrock_model_arns" {
  type    = list(string)
  default = []
}

variable "enable_point_in_time_recovery" {
  type    = bool
  default = false
}

variable "log_retention_days" {
  type    = number
  default = 14
}

variable "tags" {
  type = map(string)
  default = {
    Project     = "AI-IT-Service-Desk"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}
