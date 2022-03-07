from .base import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
   
print('produccion')

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'pgdb',
       'USER': 'pguser',
       'PASSWORD': 'password',
       'HOST': '127.0.0.1',
       'PORT': '5432',
   }
}