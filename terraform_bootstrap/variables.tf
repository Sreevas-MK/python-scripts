variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "lambda"
}

variable "project_environment" {
  description = "Project Environment"
  type        = string
  default     = "Development"
}

variable "s3_bucket_name" {
  description = "s3 bucket name"
  type        = string
  default     = "lambda-project-terraform-state-0001"
}

variable "github_username" {
  default = "Sreevas-MK"
}

variable "github_repo" {
  default = "python-scripts"
}

