from dotenv import load_dotenv
load_dotenv()

from .settings import *

DEBUG = True

MEDIA_ROOT = BASE_DIR / 'media'
DATABASES["default"]["PASSWORD"] = os.environ.get("POSTGRES_TEST_PASSWORD")

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

del STATIC_ROOT
del DATABASES["default"]["HOST"]
