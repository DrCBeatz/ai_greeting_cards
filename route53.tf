# route53.tf

resource "aws_route53_zone" "main" {
    name = var.domain_name
}

# Create an A record that points to the ALB
resource "aws_route53_record" "web_app" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name  # Use the root domain or a subdomain if needed (e.g., "www")
  type    = "A"

  alias {
    name                   = aws_lb.web_app_lb.dns_name
    zone_id                = aws_lb.web_app_lb.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "www_web_app" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.${var.domain_name}"
  type    = "CNAME"
  ttl     = 300

  records = [aws_lb.web_app_lb.dns_name]
}