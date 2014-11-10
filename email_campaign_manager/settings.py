# Django settings for email_campaign_manager project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#http://avivgr.blogspot.in/2009/05/how-to-add-remember-me-checkbox-to.html
#Path settings ] ---------
import os
PROJECT_DIR = os.path.dirname(os.path.abspath("settings.py"))
APAC_PRJ_DIR = os.path.dirname(os.path.abspath(__file__))

DJANGO_WYSIWYG_FLAVOR = "ckeditor"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':  [
        { 'name': 'document', 'items': [ 'Source', '-', 'Preview', '-', 'Templates' ] }, #// Defines toolbar group with name (used to create voice label) and items in 3 subgroups.
        { 'name': 'clipboard', 'groups': [ 'clipboard', 'undo' ], 'items': [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
        { 'name': 'editing', 'groups': [ 'find', 'selection', 'spellchecker' ], 'items': [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt' ] },
        { 'name': 'insert', 'items': [ 'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe' ] },
        '/',                                                                                    #// Line break - next group will be placed in new line.
        { 'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ], 'items': [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ] },
        { 'name': 'links', 'items': [ 'Link', 'Unlink', 'Anchor' ] },
        { 'name': 'paragraph', 'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ], 'items': [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl' ] },
        '/',
    { 'name': 'styles', 'items': [ 'Styles', 'Format', 'Font', 'FontSize' ] },
    { 'name': 'colors', 'items': [ 'TextColor', 'BGColor' ] },
    { 'name': 'tools', 'items': [ 'Maximize', 'ShowBlocks' ] },
    { 'name': 'others', 'items': [ '-' ] },
    { 'name': 'about', 'items': [ 'About' ] }

    ]
    },
}

CKEDITOR_UPLOAD_PATH = "media/ckeditor/uploads"

#Email Backend ] ---------
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Sendgrid Config ] ---------
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ECM_SENDGRID_USERNAME=EMAIL_HOST_USER
ECM_SENDGRID_PASSWORD=EMAIL_HOST_PASSWORD

ADMINS = (
     ('Hemanth Kumar A.P', 'hemanth@codelattice.com'),
)

#Asynchronous task queue  ] --------------
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379/0'

from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    'ecm_sendgrid_sync': {
        'task': 'ecm_sendgridapi.tasks.ecm_sendgridapi_dbsync',
        'schedule': crontab(minute=1, hour=0),
        #'schedule': crontab(minute='*/2'), # TESTING
    },
    'ecm_sendgrid_quota': {
        'task': 'ecm_core.tasks.sendgrid_quota_reset',
        'schedule': crontab(minute=0, hour=0, day_of_month='1'),
        # Execute every 1st dayt of month
    },
}

#Subscriptions ]-------------
ECM_DOMAIN_NAME="http://127.0.0.1:8000/"

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'ecm.sqlite'), # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

#------------------------ Change this for BIG security
ALLOWED_HOSTS = ['*'] 

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0^^!ni(x-4qv)#9ewf_k4h(-_c=hli3hb*m_b3b^77u=6=-+w3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'email_campaign_manager.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'email_campaign_manager.wsgi.application'

TEMPLATE_DIRS = (
    'templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
    "django.core.context_processors.media",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecm_core',
    'ecm_track',
    'ecm_sendgridapi',
    'django.contrib.admin',
    'south',
    'djcelery',
    'sorl.thumbnail',
    'django_wysiwyg',
    'ckeditor',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            
        },
        'ecm_console': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },

    }
}
