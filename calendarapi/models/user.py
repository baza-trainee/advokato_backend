from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

from calendarapi.extensions import (
    db,
    pwd_context,
)


class User(db.Model, UserMixin):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    description = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_superuser = db.Column(db.Boolean, default=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        hashed_password = self.hash_password(value)
        if self._password != value and self._password != hashed_password:
            self._password = hashed_password

    @classmethod
    def hash_password(cls, value):
        salt = current_app.config.get("SECRET_KEY").encode("utf-8")
        return pwd_context.hash(value, salt=salt)
