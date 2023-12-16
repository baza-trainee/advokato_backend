from re import search
from flask import flash
from flask_login import current_user
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from calendarapi.admin.common import AdminModelView
from calendarapi.admin.common import AdminModelView
from calendarapi.api.schemas import LawyerSchema
from calendarapi.extensions import db
from calendarapi.models.user import User

# async def validate_password(
#     self, password: str, user: Union[UserCreate, User]
# ) -> None:
#     if len(password) < 8:
#         raise InvalidPasswordException(reason=PASSWORD_LEN_ERROR)
#     if user.email in password:
#         raise InvalidPasswordException(reason=PASSWORD_UNIQUE_ERROR)

#     if not check_password_strength(password):
#         raise InvalidPasswordException(reason=PASSWORD_STRENGTH_ERROR)

# def check_password_strength(password: str):
#     """
#     Checks if password is a combination of
#     lowercase, uppercase, number and special symbol.
#     """
#     regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!])[A-Za-z\d@#$%^&+=!?]*$"
#     if not search(regex, password):
#         return False
#     return True


class EmailValidator:
    def __call__(self, form, field):
        schema = LawyerSchema()
        errors = schema.validate({"lawyer_mail": field.data})
        if errors.get("lawyer_mail"):
            raise ValidationError(errors["lawyer_mail"][0])


class UserModelView(AdminModelView):
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.is_superuser

    form_columns = [
        "username",
        "password",
        "confirm_password",
        "email",
        "is_active",
        # "is_superuser",
        "permissions",
        "description",
    ]
    column_list = [
        "username",
        "email",
        "is_active",
        # "is_superuser",
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
        if form.is_active.object_data and not form.is_active.data:
            if db.session.query(User).filter_by(is_active=True).count() <= 1:
                flash(
                    "Має залишитися хоча б один активний користувач.",
                    "error",
                )
                model.is_active = True
        return super().on_model_change(form, model, is_created)

    def delete_model(self, model):
        if db.session.query(User).filter_by(is_active=True).count() == 1:
            flash(
                "Має залишитися хоча б один активний користувач.",
                "error",
            )
        else:
            return super().delete_model(model)

    form_ajax_refs = {
        "permissions": {
            "fields": ("view_name",),
            "placeholder": "Доступ до розділів",
            "minimum_input_length": 0,
        },
    }
