import datetime
import logging.config
import os
import pathlib

from django.utils.translation import gettext_lazy as _

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

DEBUG = False


# Project structure

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# HTTPS

ALLOWED_HOSTS = []

CSRF_COOKIE_HTTPONLY = False

SESSION_COOKIE_HTTPONLY = False

CSRF_COOKIE_SAMESITE = os.getenv('CSRF_COOKIE_SAMESITE', 'Lax')

CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False').lower()[:1] in {'t', 'y', '1'}

SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower()[:1] in {'t', 'y', '1'}

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-window-width',
    'x-window-height',
    'cache-control',
]


# URL

BASE_URL = os.getenv('BASE_URL', 'http://localhost')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',
    }
}

CONN_MAX_AGE = 300

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Applications

TOP_PRIORITY_APPS = []

DJANGO_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
]

THIRD_PARTY_APPS = [
]

LOCAL_APPS = [
    # core apps
    'videos',
]

BOTTOM_PRIORITY_APPS = []


# Middlewares

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'unix:/var/run/rhana/memcached.sock',
        'TIMEOUT': 60 * 5,
    },
}


# Authentication - TODO: Develop a custom user model

# AUTH_USER_MODEL = 'users.User'

AUTH_USER_PASSWORD_FIELD = 'password'  # noqa: S105

AUTH_RETRY_CACHE_KEY = 'auth-retry'

AUTH_USER_ADDRESS_HEADER = 'REMOTE_ADDR'  # Used along with AUTH_RETRY_CACHE_KEY for limiting retries

AUTH_RETRY_AMOUNT = 5

AUTH_RETRY_TIMEOUT_SECONDS = 60 * 5  # 5 minutes

# Internationalization

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'pt-br')

TIME_ZONE = os.getenv('TIME_ZONE', 'America/Sao_Paulo')

USE_I18N = True

USE_TZ = True


# Static and media files

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'public_static'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

SERVE_MEDIA = False

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg']

MAX_IMAGE_SIZE_MB = 8


# Ninja

NINJA_API_TITLE = _('Rhana API')

NINJA_API_DESCRIPTION = _('Endpoint documentation for Rhana API')

NINJA_API_DOCS_URL = '/docs'

NINJA_API_DOCS_ENABLED = True

NINJA_API_NAMESPACE = 'api'

NINJA_PAGINATION_CLASS = 'ninja.pagination.PageNumberPagination'
