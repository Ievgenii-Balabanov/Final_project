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

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-book-every-5-minutes": {
        "task": "shop.tasks.add_new_books",
        "schedule": crontab(minute="*/5"),
    },
    "check-category-every-day-at-6PM": {
            'task': "shop.tasks.add_new_category",
            'schedule': crontab(minute="0", hour="18"),
        },
    "check-genre-every-day-at-6PM": {
            'task': "shop.tasks.add_new_genre",
            'schedule': crontab(minute="0", hour="18"),
        },
}
