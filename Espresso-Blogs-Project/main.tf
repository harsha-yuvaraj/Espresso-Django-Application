// Define AWS provider and set the region for resource provisioning

provider "aws" {
  region = var.REGION
}

// Create a Virtual Private Cloud to isolate the infrastructure

resource "aws_vpc" "default" {
  cidr_block           = var.AWS_VPC_CIDR_BLOCK
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "Espresso_Django_EC2_VPC"
  }
}

// Internet Gateway to allow internet access to the VPC

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
  tags = {
    Name = "Espresso_Django_EC2_Internet_Gateway"
  }
}

// Route table for controlling traffic leaving the VPC

resource "aws_route_table" "default" {
  vpc_id = aws_vpc.default.id
  route {
    cidr_block = var.AWS_ROUTE_TABLE_CIDR_BLOCK
    gateway_id = aws_internet_gateway.default.id
  }
  tags = {
    Name = "Espresso_Django_EC2_Route_Table"
  }
}

// Subnet within VPC for resource allocation

resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = var.AWS_SUBNET1_CIDR_BLOCK
  map_public_ip_on_launch = false
  availability_zone       = var.AWS_SUBNET1_AZ
  tags = {
    Name = "Espresso_Django_EC2_Subnet_1"
  }
}

// Another subnet for redundancy

resource "aws_subnet" "subnet2" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = var.AWS_SUBNET2_CIDR_BLOCK
  map_public_ip_on_launch = false
  availability_zone       = var.AWS_SUBNET2_AZ
  tags = {
    Name = "Espresso_Django_EC2_Subnet_2"
  }
}

// Associate subnets with route table for internet access
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.default.id
}
resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.default.id
}

// Security group for EC2 instance
resource "aws_security_group" "ec2_sg" {
  vpc_id = aws_vpc.default.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.AWS_SECURITY_EC2_INGRESS_CIDR] # Only allow HTTPS traffic
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.AWS_SECURITY_EC2_EGRESS_CIDR] # Allow all outbound traffic
  }
  tags = {
    Name = "Espresso_EC2_Security_Group"
  }
}

// EC2 instance for the web app

resource "aws_instance" "web" {
  ami                    = var.AWS_AMI_ID 
  instance_type          = var.AWS_INSTANCE_TYPE 
  subnet_id              = aws_subnet.subnet1.id # Place this instance in one of the private subnets
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  associate_public_ip_address = true # Assigns a public IP address to your instance
  user_data_replace_on_change = true # Replace the user data when it changes

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
    #!/bin/bash
    set -ex
    yum update -y
    yum install -y yum-utils

    # Install Docker
    yum install -y docker
    service docker start

    # Install AWS CLI
    yum install -y aws-cli

    # Authenticate to ECR
    docker login -u AWS -p $(aws ecr get-login-password --region ${var.REGION}) ${var.AWS_ECR_REPO_URI}

    # Pull the Docker image from ECR
    docker pull ${var.AWS_ECR_REPO_URI}/${var.AWS_ECR_DOCKER_IMAGE}

    # Run the Docker image
    docker run -d -p 80:8080 \
    --env SECRET_KEY=${var.SECRET_KEY} \
    --env DEBUG=${var.DEBUG} \
    --env SENDGRID_API_KEY=${var.SENDGRID_API_KEY} \
    --env DEFAULT_FROM_EMAIL=${var.DEFAULT_FROM_EMAIL} \
    --env DB_NAME=${var.DB_NAME} \
    --env DB_USER=${var.DB_USER} \
    --env DB_PASSWORD=${var.DB_PASSWORD} \
    --env DB_HOST=${var.DB_HOST} \
    --env DB_PORT=${var.DB_PORT} \
    --name espresso-django-container \
    ${var.AWS_ECR_REPO_URI}/${var.AWS_ECR_DOCKER_IMAGE}

    # Wait for Docker container to be fully up 
    sleep 10

    # Run collectstatic inside the container
    docker exec -it espresso-django-container python manage.py collectstatic --noinput
    EOF

  tags = {
    Name = "Espresso_Django_EC2_Complete_Server"
  }
}

// IAM role for EC2 instance to access ECR

resource "aws_iam_role" "ec2_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "ec2.amazonaws.com",
      },
      Effect = "Allow",
    }],
  })
}

// Attach the AmazonEC2ContainerRegistryReadOnly policy to the role

resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

// IAM instance profile for EC2 instance

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "espresso_django_ec2_complete_profile"
  role = aws_iam_role.ec2_role.name
}