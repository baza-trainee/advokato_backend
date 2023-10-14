from wtforms import DateField
from wtforms.validators import DataRequired

from calendarapi.admin.common import AdminModelView


class SheduleModelView(AdminModelView):
    column_labels = {
        "id": "id",
        "lawyers": "Адвокати",
        "time": "Доступний час",
        "date": "Дата",
    }

    column_list = [
        "id",
        "lawyers",
        "date",
        "time",
    ]

    form_columns = [
        "lawyers",
        "date",
        "time",
    ]

    form_ajax_refs = {
        "lawyers": {
            "fields": ("name",),
            "placeholder": "Оберіть адвоката",
            "minimum_input_length": 0,
        },
    }
    form_extra_fields = {
        "date": DateField(),
    }

    column_formatters = {
        "time": lambda view, context, model, name: [
            item.strftime("%H:%M") for item in model.time
        ]
        if model.time
        else ""
    }

    column_editable_list = [
        "date",
    ]

    form_args = {
        "lawyers": {
            "label": "Адвокат",
            "validators": [DataRequired()],
        }
    }
