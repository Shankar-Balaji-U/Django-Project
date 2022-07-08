"""
Django settings for HotelBillingSystem project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8opamou9t=6u+lk=4r-akl4hjs((@d(c_@x#1+kn4b!1)mtu11'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
	'CustomUser.apps.CustomuserConfig',
	'BillingSystem.apps.BillingsystemConfig',
	'Payment.apps.PaymentConfig',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'phonenumber_field',
	'crispy_forms',
	'crispy_bootstrap5',
	'fontawesomefree',
	'widget_tweaks',
	'rest_framework',
	'sass_processor',
	# 'channels',
]

MIDDLEWARE = [
	# 'django.middleware.cache.UpdateCacheMiddleware',
	# 'django.middleware.common.CommonMiddleware',
	# 'django.middleware.cache.FetchFromCacheMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HotelBillingSystem.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
					os.path.join(BASE_DIR, 'Templates'),
				],
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

WSGI_APPLICATION = 'HotelBillingSystem.wsgi.application'
ASGI_APPLICATION = 'HotelBillingSystem.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}


# Cache
# https://docs.djangoproject.com/en/4.0/topics/cache/#filesystem-caching

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': 'C:/Users/Shankar Balaji/AppData/Local/Temp/django_cache',
#     }
# }

# CACHE_MIDDLEWARE_SECONDS = 60

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

AUTH_USER_MODEL = 'CustomUser.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'd F Y'

DATETIME_FORMAT = 'd F Y, P'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'Static'),)

STATICFILES_FINDERS = [
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'sass_processor.finders.CssFinder',
]

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR,'Static')


# Media files (Images, Video, PDF)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'Media')


# Max-size of thumbnail for profile image(width, height) in CustomUser app
THUMB_SIZE = (740, 740)


# Profile image uploading file size (MIN, MAX)
PROFILE_IMAGE_SIZE = (0.5, 2)
DEFAULT_PROFILE_IMAGE_PATH = 'User profile images/default.png'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# GOOGLE_API = os.environ.get('API_KEY')


CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

PHONENUMBER_DEFAULT_REGION = "IN"


# REST_FRAMEWORK = {
# 	# Use Django's standard `django.contrib.auth` permissions,
# 	# or allow read-only access for unauthenticated users.
# 	'DEFAULT_PERMISSION_CLASSES': [
# 		'rest_framework.permissions.IsAuthenticated',
# 	],

# 	'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     ],
#     'DEFAULT_THROTTLE_CLASSES': [
#         'rest_framework.throttling.AnonRateThrottle',
#         'rest_framework.throttling.UserRateThrottle'
#     ],
#     'DEFAULT_THROTTLE_RATES': {
#         'anon': '10/hour', # also valid: second, minute, hour, day
#         'user': '15/hour',
#     },
#     'DEFAULT_FILTER_BACKENDS': [
#     	'django_filters.rest_framework.DjangoFilterBackend'
#     ]
# }


# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


LOGIN_URL = 'Login'

SIGNUP_SUCCESS_REDIRECT_URL = 'Login'
LOGIN_REDIRECT_URL = 'AddInvoice'
LOGOUT_REDIRECT_URL = 'Login'
KEEP_ME_LOGGED_IN_DURATION = 60 * 60 * 24				# (in sec.) setted to: one day