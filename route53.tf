# route53.tf

# Create the Route 53 hosted zone
resource "aws_route53_zone" "main" {
  name = var.domain_name

  lifecycle {
    prevent_destroy = true  # Prevent Terraform from deleting the hosted zone
  }
}

# Create an A record that points to the ALB
resource "aws_route53_record" "web_app" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name  # Root domain or subdomain (e.g., "www")
  type    = "A"

  alias {
    name                   = aws_lb.web_app_lb.dns_name
    zone_id                = aws_lb.web_app_lb.zone_id
    evaluate_target_health = true
  }
}

# Create a CNAME record for the www subdomain
resource "aws_route53_record" "www_web_app" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.${var.domain_name}"
  type    = "CNAME"
  ttl     = 300

  records = [aws_lb.web_app_lb.dns_name]
}
