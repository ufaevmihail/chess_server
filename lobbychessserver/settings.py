"""
Django settings for lobbychessserver project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
'''REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
CORS_ALLOW_HEADERS = (
    'xsrfheadername',
    'xsrfcookiename',
    'content-type',
    'X-CSRFTOKEN',
)'''
CORS_ALLOW_HEADERS = (
        'token',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Credentials',
        'Access-Control-Allow-Private-Network',
        'Access-Control-Allow-Origin',
    )
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000','http://192.168.0.102:3000','https://mychessapplication.herokuapp.com','http://mychessapplication.herokuapp.com']
CORS_ORIGIN_WHITELIST = ['http://localhost:3000','http://192.168.0.102:3000','https://mychessapplication.herokuapp.com','http://mychessapplication.herokuapp.com']
CSRF_COOKIE_NAME = 'XSRF-TOKEN'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
#ALLOWED_HOSTS=['localhost:8000','localhost', '127.0.0.1']
#ALLOWED_HOSTS=['*']
CSRF_COOKIE_HTTPONLY = False
'''LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'handlers': {
      'file': {
         'level': 'DEBUG',
         'class': 'logging.FileHandler',
         'filename': '/tmp/debug.log',
      },
   },
   'loggers': {
      'django': {
         'handlers': ['file'],
         'level': 'DEBUG',
         'propagate': True,
      },
   },
}'''
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
CORS_ALLOW_CREDENTIALS = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY','django-insecure-j64lmj!22x9709@-8y2eawo%0(eyte6u-7hvu&7lpm_m6!z1jx')
#SECRET_KEY = 'django-insecure-j64lmj!22x9709@-8y2eawo%0(eyte6u-7hvu&7lpm_m6!z1jx'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True) )
#DEBUG=True
ALLOWED_HOSTS = ['chess-server-app.herokuapp.com','localhost']

#SESSION_COOKIE_AGE= #in seconds
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'corsheaders',
    'lobbyserver',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lobbychessserver.urls'

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

WSGI_APPLICATION = 'lobbychessserver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ASGI_APPLICATION = "lobbychessserver.asgi.application"