from .base import *

DEBUG = False
SECRET_KEY = 'n-n4+dm-w$-d!3&uzrbxs$97-0a4)%kk@y@h(@c=g1!wxsryhg'
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}


try:
    from .local import *
except ImportError:
    pass
