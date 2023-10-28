import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

CELERY_APP = Celery('proj')

CELERY_APP.config_from_object('django.conf:settings', namespace='CELERY')

CELERY_APP.autodiscover_tasks()


@CELERY_APP.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')