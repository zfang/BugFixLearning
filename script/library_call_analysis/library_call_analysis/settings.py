DEBUG = False
DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'bugfixlearning',
         'USER': 'zfang',
         'client_encoding': 'UTF8',
         'default_transaction_isolation': 'read committed',
         'timezone': 'UTC'
         },
      'OPTIONS': {
         'autocommit': True,
         },
      }
INSTALLED_APPS = (
      'library_call_analysis'
      )
