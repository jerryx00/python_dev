from .base import *

DEBUG = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SECRET_KEY = 'n-n4+dm-w$-d!3&uzrbxs$97-0a4)%kk@y@h(@c=g1!wxsryhg'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}


# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'
