# alb.tf

resource "aws_lb" "web_app_lb" {
    name = "web-app-lb"
    internal = false
    load_balancer_type = "application"
    security_groups = [aws_security_group.lb_sg.id]
    subnets = aws_subnet.public.*.id

    enable_deletion_protection = false
}

resource "aws_lb_target_group" "web_app_tg" {
    name = "web-app-tg"
    port = 80
    protocol = "HTTP"
    vpc_id = aws_vpc.main.id
    target_type = "instance"
    health_check {
        path                = "/health"
        port                = "80"
        protocol            = "HTTP"
        interval            = 30
        timeout             = 5
        healthy_threshold   = 2
        unhealthy_threshold = 2
    }
}

resource "aws_lb_listener" "https" {
    load_balancer_arn = aws_lb.web_app_lb.arn
    port = "443"
    protocol = "HTTPS"
    ssl_policy = "ELBSecurityPolicy-2016-08"
    certificate_arn = var.ssl_certificate_arn

    default_action {
        type = "forward"
        target_group_arn = aws_lb_target_group.web_app_tg.arn
    }
}

resource "aws_lb_listener" "http" {
    load_balancer_arn = aws_lb.web_app_lb.arn
    port              = "80"
    protocol          = "HTTP"

    default_action {
        type = "redirect"
        redirect {
            protocol = "HTTPS"
            port     = "443"
            status_code = "HTTP_301"
        }
    }
}