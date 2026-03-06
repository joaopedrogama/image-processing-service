from datetime import timedelta
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
    'django_minio_backend.apps.DjangoMinioBackendConfig',
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

STORAGES = {
    "staticfiles": {
        "BACKEND": "django_minio_backend.models.MinioBackendStatic",
        "OPTIONS": {
            "MINIO_ENDPOINT": "play.min.io",
            "MINIO_ACCESS_KEY": "Q3AM3UQ867SPQQA43P2F",
            "MINIO_SECRET_KEY": "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
            "MINIO_USE_HTTPS": True,
            "MINIO_REGION": "us-east-1",
            "MINIO_URL_EXPIRY_HOURS": timedelta(days=1),  # Default is 7 days (longest) if not defined
            "MINIO_CONSISTENCY_CHECK_ON_START": True,
            "MINIO_STATIC_FILES_BUCKET": "my-static-files-bucket",
        },
    },
    "default": {
        "BACKEND": "django_minio_backend.models.MinioBackend",
        "OPTIONS": {
            "MINIO_ENDPOINT": "minio:9000",
            "MINIO_EXTERNAL_ENDPOINT": "localhost:9000",
            "MINIO_EXTERNAL_ENDPOINT_USE_HTTPS": False,
            "MINIO_ACCESS_KEY": "minioadmin",
            "MINIO_SECRET_KEY": "minioadmin",
            "MINIO_USE_HTTPS": False,
            "MINIO_REGION": "us-east-1",
            "MINIO_PRIVATE_BUCKETS": [],
            "MINIO_PUBLIC_BUCKETS": ['microservices-bucket'],
            "MINIO_URL_EXPIRY_HOURS": timedelta(days=1),  # Default is 7 days (longest) if not defined
            "MINIO_CONSISTENCY_CHECK_ON_START": False,
            "MINIO_POLICY_HOOKS": [  # List[Tuple[str, dict]]
                # ('django-backend-dev-private', dummy_policy)
            ],
            "MINIO_DEFAULT_BUCKET": "microservices-bucket",
            "MINIO_STATIC_FILES_BUCKET": "microservices-bucket",
            "MINIO_BUCKET_CHECK_ON_SAVE": False,
            # (OPTIONAL) MULTIPART UPLOAD
            "MINIO_MULTIPART_UPLOAD": False,  # False by default
            "MINIO_MULTIPART_THRESHOLD": 10 * 1024 * 1024,  # 10MB default
            "MINIO_MULTIPART_PART_SIZE": 10 * 1024 * 1024,  # 10MB default
            # (OPTIONAL) URL CACHING
            "MINIO_URL_CACHING_ENABLED": True,  # Enable URL caching (disabled by default)
            "MINIO_URL_CACHE_TIMEOUT": 60 * 60 * 8,  # 8 hours in seconds
            "MINIO_URL_CACHE_PREFIX": 'minio_url_',  # Prefix for cache keys
        },
    },
}

# Ninja

NINJA_API_TITLE = _('Rhana API')

NINJA_API_DESCRIPTION = _('Endpoint documentation for Rhana API')

NINJA_API_DOCS_URL = '/docs'

NINJA_API_DOCS_ENABLED = True

NINJA_API_NAMESPACE = 'api'

NINJA_PAGINATION_CLASS = 'ninja.pagination.PageNumberPagination'
