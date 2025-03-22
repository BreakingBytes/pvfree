from pvfree.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', '0.0.0.0']

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
PSQL_PSWD = get_secret('PSQL_PSWD', '.postgre')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PASSWORD': PSQL_PSWD,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
