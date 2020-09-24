# -*- coding: utf-8 -*-
try:
    from .celery_worker import app as celery_app
except:
    from .celery_staging import app as celery_app

__all__ = ('celery_app',)
