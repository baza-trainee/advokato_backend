from wtforms.fields import StringField
from wtforms.validators import DataRequired

from calendarapi.admin.common import AdminModelView


class UserAdminModelView(AdminModelView):
    form_extra_fields = {
        "password": StringField(
            "password", validators=[DataRequired(message="Це поле обов'язкове.")]
        )
    }
    form_columns = ["username", "email", "is_active", "password", "description"]
    column_list = ["username", "email", "is_active", "description"]
    column_exclude_list = "password"
    column_labels = {
        "email": "Email",
        "password": "Пароль",
        "is_active": "Активний",
        "description": "Опис",
        "username": "Логін",
    }

    def on_model_change(self, form, model, is_created):
        # If creating a new user, hash password
        if is_created:
            model.password = form.password.data
        else:
            # TODO
            old_password = form.password.object_data
            # If password has been changed, hash password
            if not old_password == model.password:
                model.password = form.password.data
