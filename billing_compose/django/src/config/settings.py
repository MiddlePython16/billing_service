import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

include(
    'components/database.py',
)

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',

    'rest_framework',
    'drf_spectacular',
    'django_filters',
    'corsheaders',
    'payments',

    'payment.apps.PaymentConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

JWT_PUBLIC_KEY = os.environ.get('JWT_PUBLIC_KEY')
JWT_TOKEN_LOCATION = ['headers', 'cookies']
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_PRIVATE_KEY = os.environ.get('STRIPE_PRIVATE_KEY')

YOOKASSA_ACCOUNT_ID = os.environ.get('YOOKASSA_ACCOUNT_ID')
YOOKASSA_SECRET_KEY = os.environ.get('YOOKASSA_SECRET_KEY')

PAYMENT_MODEL = 'payment.Payment'

PAYMENT_VARIANTS = {
    'stripe': (
        'payments.stripe.StripeCardProvider',
        {
            'secret_key': STRIPE_PRIVATE_KEY,
            'public_key': STRIPE_PUBLIC_KEY,
        }
    ),
    'yookassa': (
        'payment.providers.yookassa.YookassaProvider',
        {
            'account_id': YOOKASSA_ACCOUNT_ID,
            'secret_key': YOOKASSA_SECRET_KEY,
        }
    ),
    'dummy': (
        'payments.dummy.DummyProvider',
        {

        }
    )
}

PAYMENT_HOST = os.environ.get('PAYMENT_HOST', 'localhost')
PAYMENT_USES_SSL = os.environ.get('PAYMENT_USES_SSL', False)

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

AUTH_URL = os.environ.get('AUTH_URL', '127.0.0.1')
