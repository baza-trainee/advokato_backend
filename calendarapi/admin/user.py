from flask import flash
from flask_login import current_user
from wtforms import EmailField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.validators import validate_password
from calendarapi.config import PERMISSION_ALL
from calendarapi.extensions import db
from calendarapi.models.user import User
from calendarapi.commons.exeptions import (
    DATA_REQUIRED,
    INVALID_EMAIL,
    LOSS_USER_CONTROL,
    USER_IS_CURRENT,
    ZERO_ACTIVE_USER,
)


class UserModelView(AdminModelView):
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
            validators=[validate_password],
            default="test",
        ),
        "confirm_password": PasswordField(
            "Підтвердіть пароль",
            validators=[validate_password],
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
        if model.id == current_user.id:
            flash(
                USER_IS_CURRENT,
                "error",
            )
        else:
            return super().delete_model(model)

    def _validate_permissions(form, field):
        permissions = [permission.view_name for permission in field.data]
        if not ("Облікові записи" in permissions or PERMISSION_ALL in permissions):
            raise ValidationError(message=LOSS_USER_CONTROL)

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
    form_args = {
        "permissions": {
            "validators": [_validate_permissions],
        }
    }
