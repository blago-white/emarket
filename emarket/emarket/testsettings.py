from dotenv import load_dotenv
load_dotenv()

from .settings import *

DEBUG = True

del DATABASES["default"]["HOST"]
