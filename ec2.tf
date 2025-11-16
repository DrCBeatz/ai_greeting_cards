# ec2.tf

resource "aws_launch_template" "web_app" {
  name_prefix   = "web-app"
  image_id      = var.ami_id
  instance_type = var.instance_type

  tag_specifications {
    resource_type = "instance"
    tags = { Name = "web-app-ec2" }
  }

  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_instance_profile.name
  }

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.ec2_sg.id]
    subnet_id                   = aws_subnet.public[0].id
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    set -euxo pipefail
    exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

    # --- Update packages ---
    yum update -y

    # --- Install Docker, git, and SSM agent from Amazon repos ---
    yum install -y docker git amazon-ssm-agent

    systemctl enable --now docker
    systemctl enable --now amazon-ssm-agent || true

    # --- Install Docker CLI plugins (Buildx + Compose) ---
    mkdir -p /usr/libexec/docker/cli-plugins

    ARCH="$(uname -m)"
    if [ "$ARCH" = "aarch64" ]; then ARCH_DL="arm64"; else ARCH_DL="amd64"; fi

    BX_VER="v0.17.1"
    C_VER="v2.30.3"

    curl -L "https://github.com/docker/buildx/releases/download/${BX_VER}/buildx-${BX_VER}.linux-${ARCH_DL}" \
      -o /usr/libexec/docker/cli-plugins/docker-buildx
    chmod +x /usr/libexec/docker/cli-plugins/docker-buildx

    curl -L "https://github.com/docker/compose/releases/download/${C_VER}/docker-compose-linux-${ARCH}" \
      -o /usr/libexec/docker/cli-plugins/docker-compose
    chmod +x /usr/libexec/docker/cli-plugins/docker-compose

    # --- Fetch app code ---
    APP_DIR="/opt/ai_greeting_cards"
    if [ ! -d "$APP_DIR/.git" ]; then
      git clone https://github.com/DrCBeatz/ai_greeting_cards.git "$APP_DIR"
    else
      git -C "$APP_DIR" fetch --all
      git -C "$APP_DIR" reset --hard origin/main
    fi
    chown -R ec2-user:ec2-user "$APP_DIR"
    cd "$APP_DIR"

    # --- Write .env from Terraform locals ---
    cat > .env <<'EOT'
${local.env_file_content}
EOT
    chmod 600 .env

    # --- Build, migrate, and start the stack ---
    docker compose -f docker-compose.prod.yml build --pull
    docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate --noinput
    docker compose -f docker-compose.prod.yml up -d
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