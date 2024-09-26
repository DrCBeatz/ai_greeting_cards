# AI Greeting Card App

An AI-powered web application that generates personalized greeting cards using OpenAI's DALL-E 3 technology. Users can create custom images and send them via email. The app supports user authentication, payment processing for credits, and secure media storage with AWS S3.

## Table of Contents

- Features
- Prerequisites
- Installation
- Configuration
- Usage
- Testing
- Deployment
- Technologies Used
- Contributing
- License
- Contact

## Features

- AI Image Generation: Generate custom greeting card images using OpenAI's DALL-E 3 API.
- User Authentication: Secure user registration and login system.
- Payment Processing: Purchase credits using Stripe Checkout for generating images.
- Email Integration: Send generated images via email to recipients.
- Media Storage: Store images securely using AWS S3 buckets.
- Security Enhancements: Implements Content Security Policy (CSP), Django-Axes for brute-force protection, and secure headers.
- Asynchronous Tasks: Uses Celery and Redis for handling background tasks like image processing to accomodate multiple simultaneous users.

## Prerequisites

- Docker & Docker Compose: Ensure Docker and Docker Compose are installed on your machine.
- AWS Account: For S3 bucket and access keys if you plan to enable S3 storage.
- Stripe Account: For payment processing.
- OpenAI API Key: Required for image generation.
- Mailgun Account: For sending emails.

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/aigreetingcard-app.git
cd aigreetingcard-app
```

### Create .env file for Environment Variables

Create a .env file at the root of your project and populate it with the necessary environment variables below.

#### General Settings

DJANGO_SECRET_KEY=your_django_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

#### Database Settings

POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db

#### Email Settings

EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=mailgun_email_address
EMAIL_HOST_PASSWORD=mailgun_email_password
DEFAULT_FROM_EMAIL=your_default_from_email

#### OpenAI API Key

OPENAI_API_KEY=your_openai_api_key

#### Stripe Settings

STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

#### AWS S3 Settings (if using S3 for media storage)

S3_BUCKET_ENABLED=True
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
AWS_S3_REGION_NAME=your_s3_region

#### Security Settings

DJANGO_SECURE_SSL_REDIRECT=False
SECURE_PROXY_SSL_HEADER=http
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
DJANGO_SECURE_BROWSER_XSS_FILTER=False
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=False
DJANGO_SECURE_REFERRER_POLICY=same-origin
CSP_ENABLED=False
DJANGO_AXES_ENABLED=False
LOGGING_ENABLED=True

#### Celery Settings

CELERY_BROKER_URL=redis://redis:6379/0

#### Payment URLs

BACKEND_DOMAIN=your_backend_domain
PAYMENT_SUCCESS_URL=your_payment_success_url
PAYMENT_CANCEL_URL=your_payment_cancel_url
Note: Ensure you keep your secret keys secure and do not commit them to version control.

## Usage

### Build and Run Docker Containers

```bash
docker-compose up --build
```

### Apply Migrations

In a new terminal window, run:

```bash
docker-compose exec web python manage.py migrate
```

### Create a Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

### Collect Static Files

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Access the Application

Visit http://localhost:8000 in your web browser.

## Testing

### Run tests using Pytest:

```bash
docker-compose exec web pytest
```

## Deployment

For production deployment, you can use the provided docker-compose.prod.yml and Dockerfile.prod files. Ensure you set DJANGO_DEBUG=False and configure allowed hosts appropriately.

## Example Deployment Steps:

### Build the Production Image

```bash
docker-compose -f docker-compose.prod.yml build
```

### Run the Containers

```bash
docker-compose -f docker-compose.prod.yml up
```

### Apply Migrations and Collect Static Files

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## Technologies Used

- Framework: Django 4.2
- Frontend: HTML, CSS, Bootstrap 5, HTMX, Crispy Forms
- Database: PostgreSQL
- Asynchronous Tasks: Celery with Redis as broker and backend
- Payments: Stripe Checkout
- Email: SMTP via Mailgun (configurable)
- Storage: AWS S3 for media files (optional)
- Containerization: Docker & Docker Compose
- Infrastructure as Code: Terraform files included for AWS resources
- Security: Content Security Policy (CSP), Django-Axes for login attempt monitoring, Secure headers and SSL settings

## File Structure Overview

- core/: Django project settings and URLs.
- accounts/: Custom user model and authentication.
- aigreetingcards/: Main app for image generation.
- payments/: Handles payment processing with Stripe.
- templates/: HTML templates for rendering views.
- static/: Static files (CSS, JS, images).
- Dockerfile & docker-compose.yml: Configuration for Docker.
- Terraform files: Infrastructure configuration for AWS services.
