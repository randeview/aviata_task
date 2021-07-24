#!/bin/sh
container_type=${CONTAINER_TYPE-DJANGO};
celery_loglevel=${CELERY_LOGLEVEL-INFO};
if [ $container_type = "CELERY" ]; then
  celery -A config.celery_app worker -l info -c 4
elif [ $container_type = "CELERY_BEAT" ]; then
  celery -A config.celery_app beat -l info -S django
else
  python manage.py migrate --noinput
  echo "from django.contrib.auth.models import User;User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
  python manage.py list_city
  python manage.py list_directories
  python manage.py runserver 0.0.0.0:8000

fi;
