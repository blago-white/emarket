from dotenv import load_dotenv
load_dotenv()

from .settings import *

DEBUG = True

HOST_NAME = "http://127.0.0.1:8000"
CSRF_TRUSTED_ORIGINS = [HOST_NAME]

MEDIA_ROOT = BASE_DIR / 'media'
DATABASES["default"]["PASSWORD"] = os.environ.get("POSTGRES_TEST_PASSWORD")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
    }
}

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

del STATIC_ROOT
del DATABASES["default"]["HOST"]
