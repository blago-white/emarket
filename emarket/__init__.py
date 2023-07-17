import sys
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emarket.emarket.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from emarket.products.models.models import Phone
import delete_content_types

if not Phone.objects.all().exists():
    ContentType.objects.all().delete()
    os.system("python emarket/manage.py loaddata emarketdb_dump.json")
