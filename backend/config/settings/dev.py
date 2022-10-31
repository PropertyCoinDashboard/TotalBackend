from .common import *
import os

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://0.0.0.0:8080", "http://127.0.0.1:8000"]

REST_FRAMEWORK = {
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
   ),
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_DATABASE'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '3306'
    },

}

