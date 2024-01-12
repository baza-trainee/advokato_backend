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
PERMISSION_ALL = "Усі розділи"
MAIN_PAGE_URL = os.getenv("MAIN_PAGE_URL")

BABEL_DEFAULT_LOCALE = "uk_UA"

STORAGE = "STATIC"  # "STATIC" or "CLOUDINARY"
MEDIA_PATH = os.path.join("calendarapi", "static", "media")
ADMIN_CDN_URL = None  # caching static files

IMAGE_SIZE = 10
IMAGE_FORMATS = [
    "jpg",
    "jpeg",
    "png",
    "webp",
]

CACHE_TYPE = "RedisCache"
CACHE_DEFAULT_TIMEOUT = 30
CACHE_REDIS_HOST = os.getenv("CACHE_REDIS_HOST")
CACHE_REDIS_PORT = os.getenv("REDIS_PORT")
CACHE_REDIS_PASSWORD = os.getenv("REDIS_PASS")
DAY = 86400

SWAGGER_URL = "/swagger-ui"
SWAGGER_PATH = "/static/swagger.json"
SWAGGER_CONFIG = {
    "app_name": "Lawyer API",
    "syntaxHighlight.theme": "obsidian",
    "tryItOutEnabled": True,
    "requestSnippets": True,
    "displayRequestDuration": True,
}

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
    "result_expires": 3600 * 24 * 2,
    "broker_connection_retry_on_startup": True,
}

cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME", None),
    api_key=os.environ.get("API_KEY", None),
    api_secret=os.environ.get("API_SECRET", None),
)
