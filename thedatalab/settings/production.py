from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ['ebmdatalab.s2.sitereview.io', '*']

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': os.getenv('POSTGRES_DATABASE', ''),
		'USER': os.getenv('POSTGRES_USER', ''),
		'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
		'HOST': os.getenv('POSTGRES_HOST', ''),
		'PORT': os.getenv('POSTGRES_PORT', ''),
	}
}

# Use django-anymail through mailgun for sending emails
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv("MAILGUN_API_KEY", ''),
    "MAILGUN_SENDER_DOMAIN": "thedatalab.org",
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT', MEDIA_ROOT)
IMAGEFIT_ROOT = MEDIA_ROOT

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console'],
			'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
		},
	},
}
