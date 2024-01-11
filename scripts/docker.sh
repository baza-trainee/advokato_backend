#!/bin/bash


if [[ "${1}" == "celery" ]]; then
  celery -A calendarapi.celery_app:app worker -B --loglevel=info
elif [[ "${1}" == "flower" ]]; then
  celery --broker=$CELERY_BROKER_URL flower --persistent=True --basic_auth=$ADMIN_DEFAULT_LOGIN:$ADMIN_DEFAULT_PASSWORD
elif [[ "${1}" == "web" ]]; then
  gunicorn --workers 3 --threads 2 --bind=0.0.0.0:6001 --reload --log-level=debug calendarapi.wsgi:app
 fi
