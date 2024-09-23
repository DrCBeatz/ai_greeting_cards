# ai_greetings_cards

AI Greeting Card App

An AI-powered web application that generates personalized greeting cards using OpenAI's GPT technology. Users can create custom images and send them via email. The app supports user authentication, payment processing for credits, and secure media storage with AWS S3.

Table of Contents

Features
Demo
Prerequisites
Installation
Configuration
Usage
Testing
Deployment
Technologies Used
Contributing
License
Contact
Features

AI Image Generation: Generate custom greeting card images using OpenAI's API.
User Authentication: Secure user registration and login system.
Payment Processing: Purchase credits using Stripe for generating images.
Email Integration: Send generated images via email to recipients.
Media Storage: Store images securely using AWS S3 buckets.
Security Enhancements: Implements Content Security Policy (CSP), Django-Axes for brute-force protection, and secure headers.
Asynchronous Tasks: Uses Celery and Redis for handling background tasks.
Demo

If available, provide a link to a live demo or screenshots of your app.

Prerequisites

Docker & Docker Compose: Ensure Docker and Docker Compose are installed on your machine.
AWS Account: For S3 bucket and access keys if you plan to enable S3 storage.
Stripe Account: For payment processing.
OpenAI API Key: Required for image generation.
Mailgun Account: For sending emails (or modify settings for another email service).
Installation

Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/aigreetingcard-app.git
cd aigreetingcard-app
Copy Example Environment Variables
Create a .env file at the root of your project and populate it with necessary environment variables. You can use .env.example as a template if you provide one.

bash
Copy code
cp .env.example .env
Configuration

Populate the .env file with the following environment variables:

env
Copy code
# General Settings
DJANGO_SECRET_KEY=your_django_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db

# Email Settings
EMAIL_HOST_USER=your_email_username
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_default_from_email

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# Stripe Settings
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

# AWS S3 Settings (if using S3 for media storage)
S3_BUCKET_ENABLED=True
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
AWS_S3_REGION_NAME=your_s3_region

# Security Settings
CSP_ENABLED=True
DJANGO_AXES_ENABLED=True
LOGGING_ENABLED=False

# Celery Settings
CELERY_BROKER_URL=redis://redis:6379/0

# Payment URLs
BACKEND_DOMAIN=your_backend_domain
PAYMENT_SUCCESS_URL=your_payment_success_url
PAYMENT_CANCEL_URL=your_payment_cancel_url
Note: Ensure you keep your secret keys secure and do not commit them to version control.

Usage

Build and Run Docker Containers
bash
Copy code
docker-compose up --build
Apply Migrations
In a new terminal window, run:

bash
Copy code
docker-compose exec web python manage.py migrate
Create a Superuser (Optional)
bash
Copy code
docker-compose exec web python manage.py createsuperuser
Collect Static Files
bash
Copy code
docker-compose exec web python manage.py collectstatic --noinput
Access the Application
Visit http://localhost:8000 in your web browser.
Testing

Run tests using Pytest:

bash
Copy code
docker-compose exec web pytest
Deployment

For production deployment, you can use the provided docker-compose.prod.yml and Dockerfile.prod files. Ensure you set DJANGO_DEBUG=False and configure allowed hosts appropriately.

Example Deployment Steps:

Build the Production Image
bash
Copy code
docker-compose -f docker-compose.prod.yml build
Run the Containers
bash
Copy code
docker-compose -f docker-compose.prod.yml up
Apply Migrations and Collect Static Files
bash
Copy code
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
Technologies Used

Framework: Django 3.x
Frontend: HTML, CSS, Bootstrap 5, Crispy Forms
Database: PostgreSQL
Asynchronous Tasks: Celery with Redis as broker and backend
Payments: Stripe API
Email: SMTP via Mailgun (configurable)
Storage: AWS S3 for media files (optional)
Containerization: Docker & Docker Compose
Infrastructure as Code: Terraform files included for AWS resources
Security:
Content Security Policy (CSP)
Django-Axes for login attempt monitoring
Secure headers and SSL settings
File Structure Overview

core/: Django project settings and URLs.
accounts/: Custom user model and authentication.
aigreetingcards/: Main app for image generation.
payments/: Handles payment processing with Stripe.
templates/: HTML templates for rendering views.
static/: Static files (CSS, JS, images).
Dockerfile & docker-compose.yml: Configuration for Docker.
Terraform files: Infrastructure configuration for AWS services.
