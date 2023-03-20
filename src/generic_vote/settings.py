"""
Django settings for generic_vote project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from __future__ import annotations

from os import getenv, path
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY", "changeme")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DJANGO_DEBUG", False) == "True"

ALLOWED_HOSTS = getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(" ")

INTERNAL_IPS = getenv("DJANGO_INTERNAL_IPS", "127.0.0.1").split(" ")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_q",
    "app.apps.AppConfig",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "app.magic_link_auth.MagicLinkAuth",
]

ROOT_URLCONF = "generic_vote.urls"

TEMPLATES_DIR = path.join(BASE_DIR, "app", "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATES_DIR,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "generic_vote.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": path.join(BASE_DIR, "_db", "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'redis://{getenv("DJANGO_REDIS_HOST", "127.0.0.1")}:{getenv("DJANGO_REDIS_PORT", "6379")}/{getenv("DJANGO_REDIS_DB", "0")}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

Q_CLUSTER = {
    "name": "DJRedis",
    "workers": 4,
    "retry": 60,
    "timeout": 30,
    "django_redis": "default",
}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True


# Mail settings
# https://docs.djangoproject.com/en/4.1/topics/email/
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = getenv("DJANGO_EMAIL_HOST", "localhost")
EMAIL_PORT = getenv("DJANGO_EMAIL_PORT", 25)
EMAIL_HOST_USER = getenv("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = getenv("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = getenv("DJANGO_EMAIL_USE_TLS", False) == "True"
EMAIL_USE_SSL = getenv("DJANGO_EMAIL_USE_SSL", False) == "True"
DEFAULT_FROM_EMAIL = getenv("DJANGO_DEFAULT_FROM_EMAIL", "webmaster@localhost")
EMAIL_SUBJECT_PREFIX = getenv("DJANGO_EMAIL_SUBJECT_PREFIX", "[generic_vote] ")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = getenv("DJANGO_STATIC_URL", "static/")

STATIC_ROOT = path.join(BASE_DIR, "dist")

STATICFILES_DIRS = [
    path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = getenv("DJANGO_MEDIA_ROOT", "uploads/")
MEDIA_URL = getenv("DJANGO_MEDIA_URL", "uploads/")

DOMAIN = getenv("DJANGO_DOMAIN", "http://localhost:8000/")

LOGIN_URL = "app_root"
LOGIN_REDIRECT_URL = "app_root"
LOGOUT_REDIRECT_URL = "app_root"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "formatters": {
        "default": {"format": "%(asctime)s %(levelname)s %(module)s: %(message)s"},
    },
    "root": {
        "handlers": ["console"],
        "level": getenv("DJANGO_LOG_LEVEL", "INFO"),
    },
}
