"""
Django settings for idemia project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from cfenv import AppEnv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
# Default to False unless environment variable is present
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Static file settings
if DEBUG:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "idemia/static")
    STATICFILES_DIRS = [BASE_DIR / "static"]

# Set production renderer to JSONRenderer instead of the browsable API
if not DEBUG:
    REST_FRAMEWORK = {
        "DEFAULT_RENDERER_CLASSES": [
            "rest_framework.renderers.JSONRenderer",
        ]
    }

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "api.apps.IdemiaApiConfig",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "idemia.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]

WSGI_APPLICATION = "idemia.wsgi.application"


# The VCAP_APPLICATION environment variable is set by cloud.gov and
# populated with service information needed to connect to the database.
VCAP_ENV_VAR = "VCAP_APPLICATION"

if VCAP_ENV_VAR in os.environ:
    # Deployment to Cloud.gov -- Set DB to RDS
    ENV = AppEnv()
    RDS_VARS = ENV.get_service(label="aws-rds")
    DB_INFO = RDS_VARS.credentials

    DB_DICT = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_INFO["db_name"],
        "USER": DB_INFO["username"],
        "PASSWORD": DB_INFO["password"],
        "HOST": DB_INFO["host"],
        "PORT": DB_INFO["port"],
    }
else:
    # Local development -- use local DB info
    DB_DICT = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {"default": DB_DICT}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


if DEBUG:
    DEBUG_LEVEL = "DEBUG"
else:
    DEBUG_LEVEL = "INFO"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app_format": {
            "format": '{levelname}:{module}:"{message}"',
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "app_format",
        },
    },
    "loggers": {
        # unnamed logger config applies to all modules using the defualt logging.<x> calls
        "": {
            "handlers": ["console"],
            "level": DEBUG_LEVEL,
        }
    },
}
