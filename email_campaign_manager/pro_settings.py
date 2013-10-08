# Prodoction settings for apache using mod_wsgi
from settings import *

DEBUG = False
BROKER_URL = 'redis://localhost:6379/1'
ALLOWED_HOSTS = ['*']

# CKeditor ]    -------------
CKEDITOR_UPLOAD_PATH = os.path.join(APAC_PRJ_DIR, '../media/ckeditor/uploads')
CKEDITOR_UPLOAD_PREFIX = "http://127.0.0.1/media/ckeditor/uploads/" # Change this to your domain

# Sendgrid Config ] ---------
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ECM_SENDGRID_USERNAME=''
ECM_SENDGRID_PASSWORD=''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(APAC_PRJ_DIR, '../ecm.sqlite'), # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

TEMPLATE_DIRS = (
     os.path.join(APAC_PRJ_DIR, '../templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        'simple': {
            'format': '%(levelname)s %(message)s'
            },
     },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'log_file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(APAC_PRJ_DIR, '../django_ecm-consoletolog.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
            },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            
        },
        'ecm_console': {
            'handlers': ['log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },

    }
}
