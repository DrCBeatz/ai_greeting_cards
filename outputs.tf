# outputs.tf

output "alb_dns_name" {
  value = aws_lb.web_app_lb.dns_name
}

output "rds_endpoint" {
  value = aws_db_instance.web_app_db.endpoint
}
