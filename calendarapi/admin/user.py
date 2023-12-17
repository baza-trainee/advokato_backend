from flask import flash
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.validators import validate_password
from calendarapi.extensions import db
from calendarapi.models.user import User
from calendarapi.commons.exeptions import (
    BAD_EQUAL_PASSWORD,
    DATA_REQUIRED,
    INVALID_EMAIL,
    ZERO_ACTIVE_USER,
)


class UserModelView(AdminModelView):
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.is_superuser

    form_columns = [
        "username",
        "password",
        "confirm_password",
        "email",
        "is_active",
        "permissions",
        "description",
    ]
    column_list = [
        "username",
        "email",
        "is_active",
        "permissions",
        "description",
    ]
    column_exclude_list = "password"
    column_labels = {
        "email": "Пошта",
        "username": "Логін",
        "description": "Опис",
        "is_active": "Активний",
        "permissions": "Доступ до розділів #TODO",
        # "is_superuser": "superuser",
    }

    form_extra_fields = {
        "password": PasswordField(
            "Пароль",
            validators=[
                DataRequired(message=DATA_REQUIRED),
                EqualTo("confirm_password", message=BAD_EQUAL_PASSWORD),
            ],
        ),
        "confirm_password": PasswordField(
            "Підтвердіть пароль",
            validators=[
                validate_password,
                DataRequired(message=DATA_REQUIRED),
                EqualTo("password", message=BAD_EQUAL_PASSWORD),
            ],
        ),
        "email": EmailField(
            label="Пошта",
            validators=[
                Email(message=INVALID_EMAIL),
                DataRequired(message=DATA_REQUIRED),
            ],
        ),
    }

    def delete_model(self, model):
        if db.session.query(User).filter_by(is_superuser=True).count() == 1:
            flash(
                ZERO_ACTIVE_USER,
                "error",
            )
        else:
            return super().delete_model(model)

    def on_model_change(self, form, model, is_created):
        if form.is_active.object_data and not form.is_active.data:
            if db.session.query(User).filter_by(is_active=True).count() <= 1:
                flash(
                    ZERO_ACTIVE_USER,
                    "error",
                )
                model.is_active = True
        return super().on_model_change(form, model, is_created)

    form_ajax_refs = {
        "permissions": {
            "fields": ("view_name",),
            "placeholder": "Доступ до розділів",
            "minimum_input_length": 0,
        },
    }
