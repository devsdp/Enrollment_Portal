"""
Django settings for student project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+svnttkl%$=_ky-js6@)_(vpuqcsx0(6x+v)$)1&b$tni%$i2='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    # 'ajax_datatable',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    # 'user_auth.LoginCheckMiddleWare.LoginCheckMiddleWare',
]

ROOT_URLCONF = 'student.urls'

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

WSGI_APPLICATION = 'student.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# sqlite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

####mysql

DATABASES = {
'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'Student_enrollment',
       'USER': 'postgres',
    #    'PASSWORD': 'sdp150516',
        'PASSWORD': 'root',
       'HOST': '127.0.0.1',
       'PORT': '5432',
   }
}




# DATABASES = {
# 'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'masterdb',
#        'USER': 'prathamadmin',
#        'PASSWORD': 'U6uRltGf0917xISaXxez',
#        'HOST': 'enrollmentdatabase.cqtgl2j1dvta.ap-south-1.rds.amazonaws.com',
#        'PORT': '5432',
#    }
# }



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


REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES':(
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        
    ),}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL='user_auth.CustomUser'
ACCOUNT_UNIQUE_EMAIL=True

ACCOUNT_UNIQUE_EMAIL=True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_DIR=os.path.join(BASE_DIR,'static')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')    

MEDIA_URL = '/media/'
MEDIA_ROOT  = BASE_DIR/ 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Registering Custom Backend "EmailBackEnd"
# AUTHENTICATION_BACKENDS = ['user_auth.EmailBackEnd.EmailBackEnd']
