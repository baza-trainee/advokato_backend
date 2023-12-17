from datetime import datetime

from calendarapi.admin.base_admin import AdminModelView


class AppointmentModelView(AdminModelView):
    can_set_page_size = True
    can_create = False
    can_edit = True
    can_export = True
    export_types = [
        "csv",
        # "xls",
        # "xlsx",
        # "json",
        # "yaml",
        # "html",
    ]

    column_labels = {
        "lawyers": "Спеціалісти",
        "visitor": "Клієнт",
        "lawyer": "Адвокат",
        "specialization": "Спеціалізація",
        "appointment_date": "Дата",
        "appointment_time": "Час",
    }

    column_list = [
        "specialization",
        "lawyer",
        "visitor",
        "appointment_date",
    ]

    column_formatters = {
        "time": lambda view, context, model, name: [
            item.strftime("%H:%M") for item in model.time
        ]
        if model.time
        else "",
        "appointment_date": lambda view, context, model, name: datetime.combine(
            model.appointment_date, model.appointment_time
        ).strftime("%d/%m/%Y, %H:%M"),
    }

    column_searchable_list = [
        "specialization",
        "lawyer",
        "visitor",
        "appointment_date",
    ]
