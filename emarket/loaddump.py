import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emarket.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from products.models.models import Phone

if not Phone.objects.all().exists():
    ContentType.objects.all().delete()
    os.system("python manage.py loaddata ../emarketdb_dump.json")
