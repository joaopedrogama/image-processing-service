from config.settings.main import *

DEBUG = True


# HTTPS

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True


# Applications

# Email

EMAIL_USE_WHITELIST = False

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = os.getenv('EMAIL_FILE_PATH', BASE_DIR / 'mails')
