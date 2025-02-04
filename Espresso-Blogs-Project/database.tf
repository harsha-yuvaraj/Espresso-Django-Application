// DB subnet group for RDS instances, using the created subnets

resource "aws_db_subnet_group" "default" {
  subnet_ids = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]
  tags = {
    Name = "Django_EC2_Subnet_Group"
  }
}

// Security group for RDS, allows PostgreSQL traffic

resource "aws_security_group" "rds_sg" {
  vpc_id      = aws_vpc.default.id
  name        = "DjangoRDSSecurityGroup"
  description = "Allow PostgreSQL traffic"
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.AWS_RDS_EGRESS_CIDR] 
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.AWS_RDS_EGRESS_CIDR] 
  }
  tags = {
    Name = "RDS_Security_Group"
  }
}

// RDS instance for Django backend, now privately accessible

resource "aws_db_instance" "default" {
  allocated_storage      = 20
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t3.micro"
  identifier             = "espresso-django-rds"
  db_name                = var.DB_NAME
  username               = var.DB_USER
  password               = var.DB_PASSWORD
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = false
  multi_az               = false
  tags = {
    Name = "Django_RDS_Instance"
  }
}