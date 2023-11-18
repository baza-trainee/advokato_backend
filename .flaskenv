FLASK_ENV=development
FLASK_APP=calendarapi.app:create_app
SECRET_KEY=changeme
ADMIN_DEFAULT_LOGIN = admin
ADMIN_DEFAULT_PASSWORD = admin
DATABASE_URI=postgresql://default:i43RoTQIOUbk@ep-snowy-dew-05822509-pooler.us-east-1.postgres.vercel-storage.com/advocato_db
MAIN_PAGE_URL=https://statusac.com.ua

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq
CELERY_RESULT_BACKEND_URL=redis://redis

MAIL_USERNAME=calendar_api_dev@outlook.com
MAIL_PASSWORD=Calendarapi123