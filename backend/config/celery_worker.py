# -*- coding: utf-8 -*-
import logging
import os

try:
    from celery import Celery
except:
    import celery
    print(celery.__file__)
logger = logging.getLogger('Celery')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    app = Celery('config')
except:
    app = celery.Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
