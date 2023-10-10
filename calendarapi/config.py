"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

# CACHE_TYPE = "RedisCache"
# CACHE_DEFAULT_TIMEOUT = 30
# CACHE_REDIS_HOST = "redis"

SQLALCHEMY_RECORD_QUERIES = True
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY = {
    "broker_url": os.getenv("CELERY_BROKER_URL"),
    "result_backend": os.getenv("CELERY_RESULT_BACKEND_URL"),
    "broker_connection_retry_on_startup": True,
}
