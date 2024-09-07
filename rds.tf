# rds.tf

resource "aws_db_subnet_group" "main" {
  name       = "web-app-db-subnet-group"
  subnet_ids = aws_subnet.public[*].id

  tags = {
    Name = "web-app-db-subnet-group"
  }
}

resource "aws_db_instance" "web_app_db" {
    allocated_storage      = 20
    engine                 = "postgres"
    instance_class         = "db.t3.micro"
    username               = var.db_username
    password               = var.db_password
    vpc_security_group_ids = [aws_security_group.rds_sg.id]
    db_subnet_group_name   = aws_db_subnet_group.main.name
    skip_final_snapshot    = true

    lifecycle {
        prevent_destroy = true
    }
}
