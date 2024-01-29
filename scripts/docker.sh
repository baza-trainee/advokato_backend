#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery -A calendarapi.celery_app:app worker -B --loglevel=warning
elif [[ "${1}" == "flower" ]]; then
  celery --broker=$CELERY_BROKER_URL flower --persistent=True --basic_auth=$ADMIN_DEFAULT_LOGIN:$ADMIN_DEFAULT_PASSWORD
elif [[ "${1}" == "backend" ]]; then
  sleep 10
  flask db upgrade
  flask init
  gunicorn -c scripts/gunicorn.conf.py calendarapi.wsgi:app
 fi
