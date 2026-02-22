"""
Django settings for config project.
"""

import importlib.util
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_env_file(path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_env_file(BASE_DIR / '.env')


def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in {'1', 'true', 'yes', 'on'}


def module_exists(name):
    return importlib.util.find_spec(name) is not None


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production')
DEBUG = env_bool('DJANGO_DEBUG', True)
ALLOWED_HOSTS = [h.strip() for h in os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',') if h.strip()]

SITE_URL = os.getenv('DJANGO_SITE_URL', 'http://127.0.0.1:8000').rstrip('/')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'portfolio',
]

if module_exists('storages'):
    INSTALLED_APPS.append('storages')
if module_exists('rest_framework'):
    INSTALLED_APPS.append('rest_framework')
if module_exists('axes'):
    INSTALLED_APPS.append('axes')
if module_exists('django_otp'):
    INSTALLED_APPS.extend(['django_otp', 'django_otp.plugins.otp_totp'])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

if module_exists('whitenoise'):
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'portfolio.middleware.RequestRateLimitMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'portfolio.middleware.OTPEnforceMiddleware',
    'portfolio.middleware.AuditLogMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'portfolio.middleware.SecurityHeadersMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if module_exists('axes'):
    MIDDLEWARE.append('axes.middleware.AxesMiddleware')
if module_exists('django_otp'):
    MIDDLEWARE.append('django_otp.middleware.OTPMiddleware')

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'portfolio.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DB_ENGINE = os.getenv('DJANGO_DB_ENGINE', 'sqlite').lower()
if DB_ENGINE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'portfolio_db'),
            'USER': os.getenv('POSTGRES_USER', 'portfolio_user'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('POSTGRES_HOST', '127.0.0.1'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
            'CONN_MAX_AGE': int(os.getenv('POSTGRES_CONN_MAX_AGE', '60')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uz'
LANGUAGES = [
    ('uz', "O'zbekcha"),
    ('en', 'English'),
    ('ru', 'Русский'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

USE_S3 = env_bool('USE_S3', False)
if USE_S3 and module_exists('storages'):
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', '')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_QUERYSTRING_AUTH = False

    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
        },
    }

    if AWS_S3_CUSTOM_DOMAIN:
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    if module_exists('whitenoise'):
        static_backend = (
            'whitenoise.storage.CompressedManifestStaticFilesStorage'
            if not DEBUG
            else 'django.contrib.staticfiles.storage.StaticFilesStorage'
        )
        STORAGES = {
            'default': {
                'BACKEND': 'django.core.files.storage.FileSystemStorage',
            },
            'staticfiles': {
                'BACKEND': static_backend,
            },
        }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
if module_exists('axes'):
    AUTHENTICATION_BACKENDS.insert(0, 'axes.backends.AxesStandaloneBackend')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', True)
    X_FRAME_OPTIONS = 'DENY'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]

if module_exists('axes'):
    AXES_FAILURE_LIMIT = int(os.getenv('AXES_FAILURE_LIMIT', '5'))
    AXES_COOLOFF_TIME = int(os.getenv('AXES_COOLOFF_TIME', '1'))
    AXES_LOCKOUT_TEMPLATE = None

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', True)
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '20'))
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@portfolio.local')

CONTACT_THROTTLE_LIMIT = int(os.getenv('CONTACT_THROTTLE_LIMIT', '3'))
CONTACT_THROTTLE_WINDOW_SECONDS = int(os.getenv('CONTACT_THROTTLE_WINDOW_SECONDS', '600'))
GLOBAL_RATE_LIMIT_PER_MINUTE = int(os.getenv('GLOBAL_RATE_LIMIT_PER_MINUTE', '120'))
LOGIN_RATE_LIMIT_ATTEMPTS = int(os.getenv('LOGIN_RATE_LIMIT_ATTEMPTS', '5'))
LOGIN_RATE_LIMIT_WINDOW_SECONDS = int(os.getenv('LOGIN_RATE_LIMIT_WINDOW_SECONDS', '600'))
PASSWORD_RESET_RATE_LIMIT_ATTEMPTS = int(os.getenv('PASSWORD_RESET_RATE_LIMIT_ATTEMPTS', '3'))
PASSWORD_RESET_RATE_LIMIT_WINDOW_SECONDS = int(os.getenv('PASSWORD_RESET_RATE_LIMIT_WINDOW_SECONDS', '600'))

RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY', '').strip()
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY', '').strip()
RECAPTCHA_VERIFY_URL = os.getenv('RECAPTCHA_VERIFY_URL', 'https://www.google.com/recaptcha/api/siteverify').strip()
RECAPTCHA_MIN_SCORE = float(os.getenv('RECAPTCHA_MIN_SCORE', '0.3'))

BOOKING_SLOT_DAYS = int(os.getenv('BOOKING_SLOT_DAYS', '7'))
BOOKING_SLOT_HOURS = [v.strip() for v in os.getenv('BOOKING_SLOT_HOURS', '10:00,13:00,16:00').split(',') if v.strip()]
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '').strip()
TELEGRAM_USERNAME = os.getenv('TELEGRAM_USERNAME', '').strip()

HEALTHCHECK_ALERT_EMAIL = os.getenv('HEALTHCHECK_ALERT_EMAIL', '').strip()
HEALTHCHECK_ALERT_COOLDOWN_SECONDS = int(os.getenv('HEALTHCHECK_ALERT_COOLDOWN_SECONDS', '900'))

LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGOUT_REDIRECT_URL = '/'

# Signup defaults (use with caution in production).
SIGNUP_AUTO_ACTIVATE = env_bool('SIGNUP_AUTO_ACTIVATE', False)
SIGNUP_AUTO_STAFF = env_bool('SIGNUP_AUTO_STAFF', False)
SIGNUP_AUTO_SUPERUSER = env_bool('SIGNUP_AUTO_SUPERUSER', False)
if SIGNUP_AUTO_SUPERUSER:
    SIGNUP_AUTO_STAFF = True
    SIGNUP_AUTO_ACTIVATE = True
elif SIGNUP_AUTO_STAFF:
    SIGNUP_AUTO_ACTIVATE = True

CV_DOWNLOAD_URL = os.getenv('CV_DOWNLOAD_URL', '')
BOOKING_EXTERNAL_URL = os.getenv('BOOKING_EXTERNAL_URL', '')
NEWSLETTER_CAMPAIGN_PROVIDER = os.getenv('NEWSLETTER_CAMPAIGN_PROVIDER', 'none')
NEWSLETTER_CAMPAIGN_API_KEY = os.getenv('NEWSLETTER_CAMPAIGN_API_KEY', '')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', '')

SENTRY_DSN = os.getenv('SENTRY_DSN', '')
if SENTRY_DSN and module_exists('sentry_sdk'):
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.2')),
        send_default_pii=True,
    )
