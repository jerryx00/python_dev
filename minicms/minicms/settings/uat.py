from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# User Acceptance Test 测试配置
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n-n4+dm-w$-d!3&uzrbxs$97-0a4)%kk@y@h(@c=g1!wxsryhg'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
