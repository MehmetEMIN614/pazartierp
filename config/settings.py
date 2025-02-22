import os
from datetime import timedelta
from pathlib import Path

from django.utils.translation import gettext_lazy as _

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Core Settings
AUTH_USER_MODEL = "core.User"
APPEND_SLASH = False
WSGI_APPLICATION = 'config.wsgi.application'
SITE_ID = 1
ROOT_URLCONF = 'config.urls'

# URLs
FRONTEND_URL = os.environ.get('FRONTEND_URL')
BACKEND_URL = os.environ.get('BACKEND_URL')

# Internationalization
LANGUAGE_CODE = "en-us"
SUPPORTED_LANGUAGES = ["en"]
LANGUAGES = (
    ("en", _("English")),
    ("tr", _("Turkish")),
)
TIME_ZONE = "Europe/Istanbul"
USE_L10N = True
USE_TZ = True
USE_I18N = True

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
]

LOCAL_APPS = [
    'apps.core',
    'apps.accounts',
    'apps.contact',
    'apps.inventory',
    'apps.manufacturing',
    'apps.product',
    'apps.purchase',
    'apps.sales',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Base Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom
    'apps.core.middleware.audit.AuditMiddleware',

]

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get('POSTGRES_DB'),
        "USER": os.environ.get('POSTGRES_USER'),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
        "HOST": os.environ.get('POSTGRES_HOST'),
        "PORT": os.environ.get('POSTGRES_PORT'),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "connect_timeout": 10,
        }
    }
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.environ.get('JWT_SIGNING_KEY', '!2a9c@ku-detx)s05#)u_q#!x(*gpsjs=7ca8rresz**21=soq'),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    'TRAILING_SLASH': False,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',  # anonymous users
        'user': '1000/day',  # authenticated users
        'login': '1000/minute',  # login attempts
    },
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',  # Changed this line

    # Added required settings
    'FORMAT_SUFFIX_KWARG': 'format',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'NON_FIELD_ERRORS_KEY': 'error',
}

# Email Settings
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_DEFAULT_FROM_MAIL_ADDRESS')

# Storage Settings (R2 Cloudflare)
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY')
AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB

# Celery Settings
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Additional settings
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
SECRET_KEY = os.environ.get('SECRET_KEY', '+8(ra_=3@hikaromm_)uj*cw11_h5mlrj!8&q0dvy7)rffemfk')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

CORS_ORIGIN_ALLOW_ALL = True

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ["127.0.0.1"]
