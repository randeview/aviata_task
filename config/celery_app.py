import logging
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.signals import after_setup_logger
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("ctx", include=[
    'apps.core.tasks']
             )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_default_queue = "default"
app.conf.beat_schedule = {
    'every-midnight-flights': {
        'task': 'apps.core.tasks.get_flights',
        'schedule': crontab(hour=0, minute=0),
    },
    'checker-flights': {
        'task': 'apps.core.tasks.check_flight',
        'schedule': crontab(hour=1, minute=0),
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task
def test(args):
    print(args)
