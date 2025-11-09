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
    # Log everything (helps a ton during Spot replacements)
    exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

    # ---- System updates ----
    dnf -y update

    # ---- Install Docker from Docker's repo so we get buildx + compose plugins ----
    dnf -y install dnf-plugins-core
    dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
    dnf install -y \
      docker-ce docker-ce-cli containerd.io \
      docker-buildx-plugin docker-compose-plugin \
      git amazon-ssm-agent

    systemctl enable --now docker
    systemctl enable --now amazon-ssm-agent || true

    # Allow ec2-user to use docker on login shells (not needed for this script)
    usermod -aG docker ec2-user || true

    # ---- Fetch app code (idempotent) ----
    APP_DIR="/opt/ai_greeting_cards"
    if [ ! -d "$APP_DIR/.git" ]; then
      git clone https://github.com/DrCBeatz/ai_greeting_cards.git "$APP_DIR"
    else
      git -C "$APP_DIR" fetch --all
      git -C "$APP_DIR" reset --hard origin/main
    fi
    chown -R ec2-user:ec2-user "$APP_DIR"
    cd "$APP_DIR"

    # ---- Write .env from Terraform locals (quoted heredoc prevents accidental $ expansion) ----
    cat > .env <<'EOT'
${local.env_file_content}
EOT
    chmod 600 .env

    # ---- Build images locally (Buildx is present via docker-buildx-plugin) ----
    docker compose -f docker-compose.prod.yml build --pull

    # ---- Run DB migrations in a one-off container (doesn't require 'web' to be up) ----
    docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate --noinput

    # ---- Start the stack ----
    docker compose -f docker-compose.prod.yml up -d

    # Optional: if you add a healthcheck to 'web', wait for it here (example shown, commented):
    # timeout 180 bash -c 'until [ "$(docker inspect -f {{.State.Health.Status}} $(docker ps --filter "name=_web_" --format "{{.ID}}") 2>/dev/null || echo starting)" = "healthy" ]; do sleep 3; done'
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