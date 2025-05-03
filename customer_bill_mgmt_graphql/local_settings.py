import os

from .settings import *

# Local db
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "customer_bill_management_local",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,
    }
}

DEBUG = True
STATIC_ROOT = ""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIRS = [os.path.join(BASE_DIR, ""), os.path.join(BASE_DIR, "", "")]
CERILLION_END_POINT = "https://dev.exos-systems.com/app/api/getBillsForAccount"
