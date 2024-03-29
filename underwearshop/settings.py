"""
Django settings for underwearshop project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from os import getenv as env
from os import path
from dj_database_url import parse as parse_database


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    path.join(BASE_DIR, 'static'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DJANGO_DEBUG') == 'true'

ALLOWED_HOSTS = [
    env('DJANGO_ALLOWED_HOST', default='127.0.0.1')
]


# Application definition

INSTALLED_APPS = [
    'underwearshop.apps.UnderwearShopConfig',
    'django_admin_logs',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'graphene_graphiql_explorer',
    'corsheaders',
    'constance',
    'constance.backends.database',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CONSTANCE_CONFIG = {
    'PRICE_MULTIPLIER': (
        39.,
        'Every price is multiplied by this number in API and then rounded.'
    ),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware', *MIDDLEWARE
    ]

ROOT_URLCONF = 'underwearshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'underwearshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if (db_url := env('DATABASE_URL')):

    DATABASES = {'default': parse_database(db_url)}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

LANGUAGES = (
    ('ru', 'Russian'),
    ('uk', 'Ukrainian'),
)

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]

if (ENV_FRONTEND_URL := env('FRONTEND_URL')):
    CORS_ORIGIN_WHITELIST.append(ENV_FRONTEND_URL)

INTERNAL_IPS = [
    '127.0.0.1',
]

DJANGO_ADMIN_LOGS_ENABLED = False
