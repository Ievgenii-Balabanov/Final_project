import datetime
import os

from celery import Celery
from celery.schedules import crontab
from django.utils import timezone

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("worker", broker="amqp://admin:admin@localhost:5672")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "add-every-2-minutes": {
        "task": "shop.tasks.add_new_books",
        "schedule": 240.0,
        # "schedule": crontab(minute=0, hour='*/3'),
    },
    'add-every-minute': {
            'task': 'shop.tasks.add_new_category',
            'schedule': crontab(),
        },
    'add-every-two-minutes': {
            'task': 'shop.tasks.add_new_genre',
            'schedule': 120.0,
        },
    # 'add_new_order_to_warehouse': {
    #         'task': 'shop.tasks.add_order_to_warehouse',
    #         # 'schedule': 50.0,
    #         # 'args': ()
    #     },
}
