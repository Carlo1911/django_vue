# -*- coding: utf-8 -*-
import os

from config.settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')

WSGI_APPLICATION = 'config.wsgi_staging.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'db_backend'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_USER', '3ZVTwkVc9negLbmq'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': 5432,
    }
}
