FLASK_ENV=development
FLASK_APP=calendarapi.app:create_app
SECRET_KEY=changeme
ADMIN_DEFAULT_LOGIN = admin
ADMIN_DEFAULT_PASSWORD = admin
DATABASE_URI=postgresql://admin:admin@localhost:5433/calendarapi

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq
CELERY_RESULT_BACKEND_URL=redis://redis

MAIL_USERNAME=Aleshichevigor@outlook.com
MAIL_PASSWORD=45rhfy7853rt
