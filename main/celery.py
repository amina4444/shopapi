import os

from celery import Celery
from celery.beat import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_report": {
        "task": "users.tasks.send_report_mail",
        "schedule" : crontab(minute="*/5"),
    },
    "weekly_ad": {
        "task": "users.tasks.send_list_produckts",
        "schedule" : crontab(minute=0, hour=12, day_of_week='monday'),
    },
    "mounthly_statistic": {
        "task": "users.tasks.number_of_products",
        "schedule" : crontab(minute=0, hour=10, day_of_month=1),
    },
    
}
