from wtforms import EmailField
from wtforms.validators import DataRequired, ValidationError

from calendarapi.admin.common import AdminModelView
from calendarapi.api.schemas import LawyerSchema


class EmailValidator:
    def __call__(self, form, field):
        schema = LawyerSchema()
        errors = schema.validate({"lawyer_mail": field.data})
        if errors.get("lawyer_mail"):
            raise ValidationError(errors["lawyer_mail"][0])


class LawyerModelView(AdminModelView):
    can_set_page_size = True
    column_labels = {
        "name": "Ім'я",
        "specializations": "Спеціалізації",
        "specializations.specialization_name": "Спец...",
        "lawyer_mail": "Пошта",
    }
    column_sortable_list = [
        "name",
        "lawyer_mail",
    ]
    column_searchable_list = [
        "name",
        "lawyer_mail",
        "specializations.specialization_name",
    ]

    column_list = [
        "name",
        "lawyer_mail",
        "specializations",
    ]
    form_columns = [
        "name",
        "lawyer_mail",
        "specializations",
    ]

    form_ajax_refs = {
        "specializations": {
            "fields": ("specialization_name",),
            "placeholder": "Оберіть спеціалізацію",
            "minimum_input_length": 0,
        },
    }
    form_args = {
        "specializations": {
            "label": "Спеціалізації",
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        },
    }

    form_extra_fields = {
        "lawyer_mail": EmailField(
            label="Пошта",
            validators=[EmailValidator(), DataRequired("Це поле обов'язкове.")],
        ),
    }
