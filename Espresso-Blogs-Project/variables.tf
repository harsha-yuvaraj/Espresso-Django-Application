variable "REGION" {}
variable "AWS_VPC_CIDR_BLOCK" {
      sensitive = true
}
variable "AWS_ROUTE_TABLE_CIDR_BLOCK" {}
variable "AWS_SUBNET1_CIDR_BLOCK" {}
variable "AWS_SUBNET1_AZ" {}
variable "AWS_SUBNET2_CIDR_BLOCK" {}
variable "AWS_SUBNET2_AZ" {}
variable "AWS_SECURITY_EC2_INGRESS_CIDR" {  sensitive = true }
variable "AWS_SECURITY_EC2_EGRESS_CIDR"  {   sensitive = true }
variable "AWS_AMI_ID" {
      sensitive = true
}
variable "AWS_INSTANCE_TYPE" {}
variable "AWS_ECR_REPO_URI" {
      sensitive = true
}
variable "AWS_ECR_DOCKER_IMAGE" {
      sensitive = true
}
variable "AWS_RDS_EGRESS_CIDR" {}
variable "AWS_RDS_INGRESS_CIDR" {}

variable "SECRET_KEY" {
  sensitive = true
}
variable "DEBUG" { type = bool }
variable "SENDGRID_API_KEY" {
  sensitive = true
}
variable "DEFAULT_FROM_EMAIL" {}
variable "DB_NAME" {}
variable "DB_USER" {}
variable "DB_PASSWORD" {
  sensitive = true
}
variable "DB_HOST" {}
variable "DB_PORT" { type = number }
