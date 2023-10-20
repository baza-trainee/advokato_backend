from flask_login import current_user
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from calendarapi.admin.common import AdminModelView
from calendarapi.admin.common import AdminModelView
from calendarapi.api.schemas import LawyerSchema


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
            validators=[EmailValidator(), DataRequired("Це поле обов'язкове.")]
        ),
    }
