from .base import *

DEBUG = True
SECRET_KEY = 'django-insecure-f=v@tqr=v5n2bwto!o@1zgzlj6kdknfx)@2$z5cq6xed-a#()e'

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ["127.0.0.1"]
