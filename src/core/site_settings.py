import os
import sys

from .settings import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SQL_NAME = os.environ.get('TIMETRACKER_DB_NAME', 'timetracker')
SQL_HOST = os.environ.get('TIMETRACKER_DB_HOST', 'localhost')
SQL_PORT = os.environ.get('TIMETRACKER_DB_PORT', '5432')
SQL_USERNAME = os.environ.get('TIMETRACKER_DB_USER', 'root')
SQL_PASSWORD = os.environ.get('TIMETRACKER_DB_PASSWORD', 'password')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SQL_NAME,
        'USER': SQL_USERNAME,
        'PASSWORD': SQL_PASSWORD,
        'HOST': SQL_HOST,
        'PORT': SQL_PORT,
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')


if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]


if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
