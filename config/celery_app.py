import logging
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.signals import after_setup_logger


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("ctx")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_default_queue = "default"

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

