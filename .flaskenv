FLASK_ENV=development
FLASK_APP=calendarapi.app:create_app
SECRET_KEY=changeme
ADMIN_DEFAULT_LOGIN = admin
ADMIN_DEFAULT_PASSWORD = admin
DATABASE_URI=postgresql://admin:admin@localhost:5432/calendarapi
MAIN_PAGE_URL=https://statusac.com.ua

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq
CELERY_RESULT_BACKEND_URL=redis://redis

MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USERNAME = syniava.roksolan1996@gmail.com
MAIL_PASSWORD = uimxjctqcgexixvu

