from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qcsystem.settings')

app = Celery('qcsystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check_monthly_scrap_rate' :{
        'task': 'reports.tasks.check_monthly_scrap_rate',
        'schedule': crontab(minute=0, hour=0, day_of_month='1')
    }
}