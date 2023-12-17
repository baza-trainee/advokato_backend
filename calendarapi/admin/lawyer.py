from wtforms import EmailField
from wtforms.validators import DataRequired, Email

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.commons.exeptions import DATA_REQUIRED, INVALID_EMAIL


class LawyerModelView(AdminModelView):
    can_set_page_size = True
    column_labels = {
        "name": "Ім'я",
        "specializations": "Спеціалізації",
        "specializations.specialization_name": "Спеціалізація",
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
            "validators": [DataRequired(message=DATA_REQUIRED)],
        },
    }

    form_extra_fields = {
        "lawyer_mail": EmailField(
            label="Пошта",
            validators=[
                Email(message=INVALID_EMAIL),
                DataRequired(message=DATA_REQUIRED),
            ],
        ),
    }
