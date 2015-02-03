"""
Django settings for mysy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import urlparse
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1#e7y%z@c&ii4_n1w47^2f@a526n3y3e@_8i_p25&mdm4xe5-w'

# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = True

DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
        '.nitrousbox.com',
        '.rhcloud.com',
    ]

ON_OPENSHIFT = False 

if os.environ.has_key('OPENSHIFT_REPO_DIR'):     
    ON_OPENSHIFT = True

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

#if ON_OPENSHIFT:
#    DEBUG=False
#else:
#    DEBUG=True



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysy.urls'

WSGI_APPLICATION = 'mysy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


if ON_OPENSHIFT:
    url = urlparse.urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
         }
    }
else: 
    DATABASES = {
    	'default': {
        	'ENGINE': 'django.db.backends.mysql',
        	'NAME': 'mysy',
        	'USER': 'root',
		'HOST': '0.0.0.0',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_DIR, '..', '..', 'static')

STATIC_URL = '/static/'

#ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_FINDERS = (
     'django.contrib.staticfiles.finders.FileSystemFinder',
     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
 #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
 )
