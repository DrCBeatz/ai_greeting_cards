# ec2.tf

resource "aws_launch_template" "web_app" {
    name_prefix = "web-app"
    image_id = var.ami_id
    instance_type = var.instance_type

    iam_instance_profile {
        name = aws_iam_instance_profile.ec2_instance_profile.name
    }

    network_interfaces {
        associate_public_ip_address = true
        security_groups = [aws_security_group.ec2_sg.id]
        subnet_id = aws_subnet.public[0].id # Specify the public subnet
    }

    user_data = base64encode(<<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum -y install docker
    sudo service docker start
    sudo systemctl enable docker
    sudo usermod -a -G docker ec2-user
    sudo chmod 666 /var/run/docker.sock
    sudo yum install git -y
    sudo yum install -y amazon-ssm-agent  # Install SSM agent
    sudo systemctl enable amazon-ssm-agent
    sudo systemctl start amazon-ssm-agent

    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    git clone https://github.com/DrCBeatz/ai_greeting_cards.git
    cd ai_greeting_cards
    sudo chown -R $(whoami):$(whoami) /ai_greeting_cards

    cat <<EOT >> .env
    ${local.env_file_content}
    EOT
    sudo chmod a+w .env
    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
  EOF
  )              
}

resource "aws_autoscaling_group" "web_app_asg" {
    desired_capacity = 1
    max_size = 3
    min_size = 1
    vpc_zone_identifier = aws_subnet.public.*.id

    mixed_instances_policy {
        launch_template {
            launch_template_specification {
                launch_template_id = aws_launch_template.web_app.id
                version = "$Latest"
            }
            override {
                instance_type = var.instance_type
            }
        }

        instances_distribution {
            on_demand_base_capacity = 0
            on_demand_percentage_above_base_capacity = 0
            spot_allocation_strategy = "lowest-price"
        }
    }
    

    target_group_arns = [aws_lb_target_group.web_app_tg.arn]
    health_check_type = "EC2"
    health_check_grace_period = 300
}