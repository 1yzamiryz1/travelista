from mysite.settings import *
from secretvariables import secret_key, db_password

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['1amiryz1.ir', 'www.1amiryz1.ir']

# INSTALLED_APPS = []

# sites framework
SITE_ID = 3

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": 'amiryzir_1amiryz1',
        "USER": "amiryzir_amir",
        "PASSWORD": db_password,
        "HOST": 'localhost',
        "PORT": '3306',
    }
}

STATIC_ROOT = "/home/amiryzir/public_html/static"
MEDIA_ROOT = "/home/amiryzir/public_html/media"

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]

MAINTENANCE_MODE = False

## X-Frame-Options
X_FRAME_OPTIONS = 'DENY'
# X-Content-Type-Options
SECURE_CONTENT_TYPE_NOSNIFF = True
## Strict-Transport-Security
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

## that requests over HTTP are redirected to HTTPS. aslo can config in webserver
SECURE_SSL_REDIRECT = True

# for more security
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Strict'
