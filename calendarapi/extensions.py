"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import marshmallow

from flask_mail import Mail


from calendarapi.commons.apispec import APISpecExt


ma = marshmallow
db = SQLAlchemy()
fm = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
mail = Mail()
