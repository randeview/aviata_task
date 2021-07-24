#!/bin/sh
container_type=${CONTAINER_TYPE-DJANGO};
celery_loglevel=${CELERY_LOGLEVEL-INFO};
if [ $container_type = "CELERY" ]; then
  celery -A config.celery_app worker -l info -c 4
elif [ $container_type = "CELERY_BEAT" ]; then
  celery -A config.celery_app beat -l info -S django
else
  python manage.py reasons_sms_populate
  python manage.py migrate --noinput
  uwsgi --ini /app/config/server/uwsgi.ini
fi;
