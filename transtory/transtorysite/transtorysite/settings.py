"""
Django settings for transtorysite project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Apps database path
APPS_DATABASE_DIR = r"C:\Users\Wei\OneDrive\Wei_Project\transtory\database"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h=k=ku*&jk*_8ej=e^kmkj+1j3q4%(#s0@hd^%8p1f!dvtani#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'mobike.apps.MobikeConfig',
    'shanghaimetro.apps.ShanghaimetroConfig',
    'crh.apps.CrhConfig',
    'flight.apps.FlightConfig',
    'django_tables2',
    'bootstrap3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'transtorysite.urls'

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

WSGI_APPLICATION = 'transtorysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'mobike_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(APPS_DATABASE_DIR, 'mobike', 'MobikeTrips.sqlite'),
    },
    'shanghaimetro_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(APPS_DATABASE_DIR, 'shanghaimetro', 'ShanghaiMetroTrips.sqlite'),
    },
    'crh_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(APPS_DATABASE_DIR, 'crh', 'CrhTransits.sqlite'),
    },
    'flight_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(APPS_DATABASE_DIR, 'flight', 'FlightTransits.sqlite'),
    }
}

DATABASE_ROUTERS = [
    'mobike.routers.MobikeDatabaseRouter',
    'shanghaimetro.routers.ShanghaimetroDatabaseRouter',
    'crh.routers.CrhDatabaseRouter',
    'flight.routers.FlightDatabaseRouter'
]


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
