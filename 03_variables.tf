variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "lambda-project"
}

variable "project_environment" {
  description = "Project Environment"
  type        = string
  default     = "Development"
}

variable "github_username" {
  default = "Sreevas-MK"
}

variable "github_repo" {
  default = "python-scripts"
}
