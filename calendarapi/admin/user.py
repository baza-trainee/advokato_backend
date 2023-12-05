from flask import flash
from flask_login import current_user
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from calendarapi.admin.common import AdminModelView
from calendarapi.admin.common import AdminModelView
from calendarapi.api.schemas import LawyerSchema
from calendarapi.extensions import db
from calendarapi.models.user import User


class EmailValidator:
    def __call__(self, form, field):
        schema = LawyerSchema()
        errors = schema.validate({"lawyer_mail": field.data})
        if errors.get("lawyer_mail"):
            raise ValidationError(errors["lawyer_mail"][0])


class UserAdminModelView(AdminModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_superuser

    form_columns = [
        "username",
        "password",
        "confirm_password",
        "email",
        "is_active",
        "is_superuser",
        "description",
    ]
    column_list = [
        "username",
        "email",
        "description",
        "is_active",
        "is_superuser",
    ]
    column_exclude_list = "password"
    column_labels = {
        "email": "Пошта",
        "username": "Логін",
        "description": "Опис",
        "is_active": "Активний",
        "is_superuser": "superuser",
    }

    form_extra_fields = {
        "password": PasswordField(
            "Пароль",
            validators=[
                DataRequired(message="Це поле обов'язкове."),
                EqualTo("confirm_password", message="Паролі повинні співпадати"),
            ],
        ),
        "confirm_password": PasswordField(
            "Підтвердіть пароль",
            validators=[
                DataRequired(message="Це поле обов'язкове."),
                EqualTo("password", message="Паролі повинні співпадати"),
            ],
        ),
        "email": EmailField(
            label="Пошта",
            validators=[EmailValidator(), DataRequired("Це поле обов'язкове.")],
        ),
    }

    def delete_model(self, model):
        if db.session.query(User).filter_by(is_superuser=True).count() == 1:
            flash(
                "Має залишитися хоча б один користувач із привілегією superuser",
                "error",
            )
        else:
            return super().delete_model(model)

    def on_model_change(self, form, model, is_created):
        if form.is_superuser.object_data and not form.is_superuser.data:
            if db.session.query(User).filter_by(is_superuser=True).count() <= 1:
                flash(
                    "Має залишитися хоча б один користувач із привілегією superuser",
                    "error",
                )
                model.is_superuser = True
        return super().on_model_change(form, model, is_created)

    def delete_model(self, model):
        if db.session.query(User).filter_by(is_superuser=True).count() == 1:
            flash(
                "Має залишитися хоча б один користувач із привілегією superuser",
                "error",
            )
        else:
            return super().delete_model(model)
