from .common import *
import os

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "http://0.0.0.0:8080",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8081",
]
DEBUG = True


REST_FRAMEWORK = {
    ###'NON_FIELD_ERRORS_KEY': 'error',###  요거 제외밑에부터
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

DATABASES = {
    "coin": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_DATABASE"),
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": "3306",
    },
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("auth_DB_DATABASE"),
        "USER": os.getenv("auth_DB_USERNAME"),
        "PASSWORD": os.getenv("auth_DB_PASSWORD"),
        "HOST": os.getenv("auth_DB_HOST"),
        "PORT": "3306",
    }
}
