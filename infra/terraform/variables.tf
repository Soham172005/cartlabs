variable "project_name" {
  description = "Project name used for AWS resource tags."
  type        = string
  default     = "cartlabs"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "AWS region for the deployment."
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "Single EC2 instance type for CartLabs."
  type        = string
  default     = "m5.large"
}

variable "key_name" {
  description = "Existing AWS EC2 key pair name for SSH access."
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to SSH into the instance. Use your public IP with /32."
  type        = string
}

variable "allowed_http_cidr" {
  description = "CIDR allowed to access HTTP/app ports."
  type        = string
  default     = "0.0.0.0/0"
}

variable "root_volume_size" {
  description = "Root EBS volume size in GiB."
  type        = number
  default     = 30
}
