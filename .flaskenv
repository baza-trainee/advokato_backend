FLASK_ENV=development
FLASK_APP=calendarapi.app:create_app
SECRET_KEY=changeme
DATABASE_URI=postgresql://admin:admin@postgres:5432/calendarapi

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq
CELERY_RESULT_BACKEND_URL=redis://redis
