from .common import *
import os

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://0.0.0.0:8080", "http://127.0.0.1:8000"]


# ##db라우터
# DATABASE_ROUTERS = [
#     'config.settings.dbrouter.MultiDBRouter',
# ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_DATABASE'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '3306'
    },
    # 'auth_user_db': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}
