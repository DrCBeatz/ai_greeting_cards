# locals.tf

locals {
  env_file_content = file("${path.module}/.env.prod")
}