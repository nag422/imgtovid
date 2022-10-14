import os
from .dbconfig import DATABASES,DATABASES1
from dotenv import load_dotenv
load_dotenv()


IMAGE_PROCESSING_URL="E:/imgtovid/videorender/static/"
IMAGE_PROCESSING_ROOT="E:/imgtovid/videorender/media/post_images/"
IMAGE_PROCESSING_EXCEL="E:/imgtovid/videorender"

MONGO_URL = os.getenv("MONGO_URL")
CLIENT_KEY_YTUBE = os.getenv("CLIENT_KEY_YTUBE")
SEX_WORD = os.getenv("SEX_WORD_MODULE")
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv('GOOGLE_RECAPTCHA')
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_DIR = os.path.join(BASE_DIR, 'videoapp','templates', 'react','static')
STATIC_DIR = os.path.join(BASE_DIR,'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SEX_WORD

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'videoapp',
    'telegrambox',
    'livedash',
    'wordpressrest',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders', 
    'rest_auth',
    'django.contrib.sites',
    'mathfilters',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'django_apscheduler',
    
    # 'channels'
    # 'allauth',
    # 'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]
#CORS_ORIGIN_WHITELIST = ['http://203.217.145.24']

ROOT_URLCONF = 'videorender.urls'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# APSCHEDULER_DATETIME_FORMAT =  "N j, Y, f:s a"  # Default

# AUTHENTICATION_BACKENDS = (
    
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',

#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend'
    
# )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
    #    'rest_framework_simplejwt.authentication.JWTAuthentication'
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     #'rest_framework.permissions.IsAuthenticated',
    #     # 'rest_framework.permissions.AllowAny',
    #     'rest_framework.authentication.BasicAuthentication'
    # ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'static'),os.path.join(BASE_DIR,'telegrambox/templates')],
        # 'DIRS': [os.path.join(BASE_DIR,'static')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'videorender.wsgi.application'
# ASGI_APPLICATION = "feedbox.routing.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''

DATABASES = DATABASES


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


CRISPY_TEMPLATE_PACK = 'bootstrap4'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [STATIC_DIR]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_HOST ="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER="wahdigitalsocialmedia@gmail.com"
EMAIL_HOST_PASSWORD="@VoletiReel"
EMAIL_USE_TLS=True
CACHE_TTL = 60 * 1

CACHES = {
    "default":{
        'BACKEND': "django_redis.cache.RedisCache",
        'LOCATION': "redis://127.0.0.1:6379/1"
    }
}

SITE_ID = 1
#LOGIN_REDIRECT_URL = '/oauthlogin'

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = False