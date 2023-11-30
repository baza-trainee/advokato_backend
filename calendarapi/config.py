"""Default configuration

Use env var to override
"""
import os
import cloudinary

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_DEFAULT_LOGIN = os.getenv("ADMIN_DEFAULT_LOGIN")
ADMIN_DEFAULT_PASSWORD = os.getenv("ADMIN_DEFAULT_PASSWORD")
MAIN_PAGE_URL = os.getenv("MAIN_PAGE_URL")

BABEL_DEFAULT_LOCALE = "uk_UA"

# CACHE_TYPE = "RedisCache"
# CACHE_DEFAULT_TIMEOUT = 30
# CACHE_REDIS_HOST = "redis"

MAIL_DEFAULT_SENDER = MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")

SQLALCHEMY_RECORD_QUERIES = True
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY = {
    "broker_url": os.getenv("CELERY_BROKER_URL"),
    "result_backend": os.getenv("CELERY_RESULT_BACKEND_URL"),
    "broker_connection_retry_on_startup": True,
}

cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)