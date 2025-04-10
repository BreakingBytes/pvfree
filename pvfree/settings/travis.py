from pvfree.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', '0.0.0.0']

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
TRAVIS_PASSWORD = get_secret('TRAVIS_PASSWORD', '.travis_password')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travis_ci_test',
        'USER': 'travis',
        'PASSWORD': TRAVIS_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
