from wtforms import EmailField
from wtforms.validators import DataRequired, Email

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.commons.exeptions import DATA_REQUIRED, INVALID_EMAIL, REQ_MAX_LEN
from calendarapi.models.lawyer import Lawyer


NAME_LEN = Lawyer.name.type.length


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
        "name": {"description": REQ_MAX_LEN % NAME_LEN},
        "specializations": {
            "label": "Спеціалізації",
            "validators": [DataRequired(message=DATA_REQUIRED)],
            "description": "Можна обрати декілька спеціалізацій",
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
