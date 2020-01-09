provider "aws" {
  region = "us-east-1"
}

resource "aws_db_instance" "default" {
  name                 = "postgres_db"
  engine               = "postgres"
  instance_class       = "db.t2.micro"
  allocated_storage    = 20
  storage_type         = "gp2"
  username             = "foo"
  password             = "password123"
  db_subnet_group_name = "default-vpc-0ae7dc15b87a40a07"
}

resource "null_resource" "update_password" {
  provisioner "local-exec" {
    command = "python3 update_password.py --db_identifier=${aws_db_instance.default.identifier}"
  }
}