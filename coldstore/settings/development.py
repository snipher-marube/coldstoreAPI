from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS =['127.0.0.1', 'localhost']
DOMAINS = ['localhost', '127.0.0.1']
SECURE_SSL_REDIRECT = False
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'agrotech_db',
        'USER': 'snipher',
        'PASSWORD': 'snipher8431',
        'HOST': 'localhost',
        'PORT': '5432',
        
    }
}
