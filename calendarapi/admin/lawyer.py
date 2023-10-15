from wtforms.validators import DataRequired, ValidationError

from calendarapi.admin.common import AdminModelView
from calendarapi.api.schemas import LawyerSchema


class EmailValidator:
    def __call__(self, form, field):
        schema = LawyerSchema()
        errors = schema.validate({"lawyer_mail": field.data})
        if errors.get("lawyer_mail"):
            raise ValidationError(errors["lawyer_mail"][0])


class LawyerAdminModelView(AdminModelView):
    column_labels = {
        "name": "Ім'я",
        "surname": "Прізвище",
        "lawyer_mail": "Пошта",
        "cities": "Місто",
        "specializations": "Спеціалізації",
    }

    column_list = [
        "name",
        "surname",
        "lawyer_mail",
        "cities",
        "specializations",
    ]
    form_columns = [
        "name",
        "surname",
        "lawyer_mail",
        "cities",
        "specializations",
    ]

    form_ajax_refs = {
        "specializations": {
            "fields": ("specialization_name",),
            "placeholder": "Оберіть спеціалізацію",
            "minimum_input_length": 0,
        },
        "cities": {
            "fields": ("city_name",),
            "placeholder": "Оберіть місто",
            "minimum_input_length": 0,
        },
    }
    form_args = {
        "specializations": {
            "label": "Спеціалізації",
            "validators": [DataRequired()],
        },
        "cities": {
            "label": "Місто",
            "validators": [DataRequired()],
        },
        "lawyer_mail": {
            "validators": [EmailValidator()],
        },
    }
