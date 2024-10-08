# core/settings.py

import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()

# OpenAI API Key
OPENAI_API_KEY = env('OPENAI_API_KEY')

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Debug mode
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# Allowed hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default="*")

# Admin URL
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

# CSP enabled env variable
CSP_ENABLED = env.bool("CSP_ENABLED", default=True)

# Logging Enabled env variable
LOGGING_ENABLED = env.bool("LOGGING_ENABLED", default=False)

# Django Axes enabled env variable
DJANGO_AXES_ENABLED = env.bool("DJANGO_AXES_ENABLED", default=True)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'django_cleanup.apps.CleanupConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'csp',
    'axes',
    'django_celery_results',
    'storages',
    # Local apps
    'accounts.apps.AccountsConfig',
    'aigreetingcards',
    'payments',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

if CSP_ENABLED:
    index = MIDDLEWARE.index('django.contrib.messages.middleware.MessageMiddleware')
    MIDDLEWARE.insert(index, 'csp.middleware.CSPMiddleware')

# Root URL configuration
ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'core.wsgi.application'

# Database configuration
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_HOST = env.str("POSTGRES_HOST")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': '5432',
    }
}

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='webmaster@localhost.com')

if LOGGING_ENABLED:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'psycopg': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGOUT_REDIRECT_URL = 'image_list'

# Custom user model
AUTH_USER_MODEL = "accounts.CustomUser"

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# S3 Bucket settings
S3_BUCKET_ENABLED = env.bool("S3_BUCKET_ENABLED", default=False)
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-2')
AWS_QUERYSTRING_AUTH = False  # Disable URL query strings for media files

# Media files
if not S3_BUCKET_ENABLED:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Links for Payments app
BACKEND_DOMAIN = env("BACKEND_DOMAIN")
PAYMENT_SUCCESS_URL = env("PAYMENT_SUCCESS_URL")
PAYMENT_CANCEL_URL = env("PAYMENT_CANCEL_URL")

# Stripe
STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET")

# Django-Axes settings

AXES_ENABLED = DJANGO_AXES_ENABLED
AXES_FAILURE_LIMIT = 10
AXES_LOCK_OUT_AT_FAILURE = True

# django-csp headers:

if CSP_ENABLED:
    CSP_STYLE_SRC = (
        "'self'",
        "use.fontawesome.com",
        "cdnjs.cloudflare.com",
        "fonts.googleapis.com",
    )

    CSP_SCRIPT_SRC = ("'self'",)

    CSP_IMG_SRC = (
        "'self'",
        "ai-greeting-cards-media.s3.amazonaws.com",
        "data:",
        "blob:",
    )

    CSP_FONT_SRC = (
        "'self'",
        "cdnjs.cloudflare.com",
        "fonts.gstatic.com",
        "fonts.googleapis.com",
        "data:",
    )

    CSP_CONNECT_SRC = ("'self'",)
    CSP_OBJECT_SRC = ("'none'",)
    CSP_BASE_URI = ("'self'",)
    CSP_FRAME_ANCESTORS = "'self'"
    CSP_FORM_ACTION = ("'self'", "checkout.stripe.com")
    CSP_INCLUDE_NONCE_IN = ("script-src", "style-src")
    CSP_MANIFEST_SRC = ("'self'",)
    CSP_WORKER_SRC = ("'self'",)
    CSP_MEDIA_SRC = ("'self'",)
    CSP_CONNECT_SRC = ("'self'",)
    CSP_DEFAULT_SRC = ("'none'",)

# Security settings for production
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False) # Set to False in production because ALB handles SSL termination
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
SECURE_BROWSER_XSS_FILTER = env.bool("DJANGO_SECURE_BROWSER_XSS_FILTER", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_REFERRER_POLICY = env("DJANGO_SECURE_REFERRER_POLICY", default="no-referrer-when-downgrade")


# Celery Configuration
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
