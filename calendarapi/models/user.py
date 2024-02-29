from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

from calendarapi.extensions import db, pwd_context


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column("password", db.String(1024), nullable=False)
    description = db.Column(db.String(2000), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    permissions = db.relationship(
        "Permission",
        secondary="users_to_permissions",
        lazy=True,
        backref=db.backref("users", lazy=True),
    )

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
