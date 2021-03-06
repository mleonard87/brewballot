"""
Django settings for brewballot project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, json

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

secrets_json = None

def get_secret_json(setting, default=None):
    """Get the secret variable of return an explicit exception"""
    try:
        return secrets_json[setting]
    except KeyError:
        if default:
            return default
        error_msg = "Set the {0} property in secrets.json".format(setting)
        raise ImproperlyConfigured(error_msg)

def get_secret_env(setting, default=None):
    """Get the secret variable of return an explicit exception"""
    try:
        return os.environ[setting]
    except KeyError:
        if default:
            return default
        error_msg = "Set the {0} property in an environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

get_secret = None
if os.path.isfile(os.path.join(BASE_DIR, 'settings', 'secrets.json')):
    with open(os.path.join(BASE_DIR, 'settings', 'secrets.json')) as f:
        secrets_json = json.loads(f.read())
    get_secret = get_secret_json
else:
    get_secret = get_secret_env


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'poll',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'brewballot.urls'

WSGI_APPLICATION = 'brewballot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    'templates',
    )

STATICFILES_DIRS = (
    ('js', 'static/jquery-2.1.1'),
    ('css', 'static/css'),
    ('img', 'static/images'),
    ('audio', 'static/audio'),
)

TWILIO_ACCOUNT_SID = get_secret('TWILIO_ACCOUNT_SID')

TWILIO_AUTH_TOKEN = get_secret('TWILIO_AUTH_TOKEN')

VOTE_SMS_NUMBER = get_secret('VOTE_SMS_NUMBER')