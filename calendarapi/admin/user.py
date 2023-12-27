from flask import flash
from flask_login import current_user
from sqlalchemy import and_, func, or_
from wtforms import EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, StopValidation

from calendarapi.extensions import db
from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.validators import validate_password
from calendarapi.admin.commons.descriptions import EMPTY_EDIT_FIELD
from calendarapi.models.user import User
from calendarapi.config import PERMISSION_ALL
from calendarapi.commons.exeptions import (
    DATA_REQUIRED,
    INVALID_EMAIL,
    LOSS_USER_CONTROL,
    DELETE_CURRENT_USER,
    REQ_MAX_LEN,
    REQ_PASSWORD,
    ZERO_ACTIVE_USER,
    ZERO_PERMISSION_USER,
)
from calendarapi.models.user_permissions import Permission

USERNAME_LEN = User.username.type.length
DESCRIPTION_LEN = User.description.type.length


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
        "description": "Замітки",
        "is_active": "Активний",
        "permissions": "Доступ до розділів",
    }

    form_extra_fields = {
        "password": PasswordField(
            "Пароль",
            validators=[
                DataRequired(message=DATA_REQUIRED),
                validate_password,
            ],
            description=REQ_PASSWORD,
        ),
        "confirm_password": PasswordField(
            "Підтвердіть пароль",
            validators=[
                DataRequired(message=DATA_REQUIRED),
                validate_password,
            ],
        ),
        "email": EmailField(
            label="Пошта",
            validators=[
                Email(message=INVALID_EMAIL),
                DataRequired(message=DATA_REQUIRED),
            ],
            description="Необхідна для відновлення паролю.",
        ),
        "description": TextAreaField(
            label="Замітки",
            render_kw={
                "class": "form-control",
                "rows": 3,
                "maxlength": DESCRIPTION_LEN,
            },
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=REQ_MAX_LEN % DESCRIPTION_LEN,
        ),
    }

    def edit_form(self, obj=None):
        form = super(UserModelView, self).edit_form(obj)
        form.view_name = self.name
        form.password.description = form.confirm_password.description = EMPTY_EDIT_FIELD
        form.password.validators = form.confirm_password.validators = [
            validate_password
        ]
        form.password.flags.required = form.confirm_password.flags.required = False
        return form

    def delete_model(self, model):
        if model.id == current_user.id:
            query = (
                db.session.query(User)
                .join(User.permissions)
                .filter(
                    and_(
                        User.is_active == True,
                        or_(
                            Permission.view_name.ilike(f"%{self.name}%"),
                            Permission.view_name.ilike(f"%{PERMISSION_ALL}%"),
                        ),
                    )
                )
            )
            if query.count() <= 1:
                flash(
                    ZERO_PERMISSION_USER,
                    "error",
                )
            else:
                return super().delete_model(model)
        else:
            return super().delete_model(model)

    def _validate_permissions(form, field):
        permissions = [permission.view_name for permission in field.data]
        if (
            form._obj
            and form._obj.id == current_user.id
            and not (form.view_name in permissions or PERMISSION_ALL in permissions)
        ):
            field.data = field.object_data
            raise StopValidation(message=LOSS_USER_CONTROL)

    def on_model_change(self, form, model, is_created):
        if form.is_active.object_data and not form.is_active.data:
            if self.session.query(User).filter_by(is_active=True).count() <= 1:
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
            "description": 'У користувача буде доступ лише для обраних розділів. Оберіть "Усі розділи" якщо бажаєте надати повний доступ.',
        },
        "is_active": {
            "description": "Якщо вимкнути - користувач не зможе увійти в панель адміністратора.",
        },
        "username": {"description": REQ_MAX_LEN % USERNAME_LEN},
    }
