from calendarapi.admin.base_admin import AdminModelView


class VisitorModelView(AdminModelView):
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
        "id": "ID Клієнта",
        "name": "ім'я",
        "phone_number": "Мобільний",
        "email": "Пошта",
        "is_beneficiary": "Пільговик",
    }

    column_formatters = {
        "is_beneficiary": lambda view, context, model, name: "так"
        if model.is_beneficiary
        else "ні",
    }

    column_searchable_list = [
        "name",
        "email",
        "phone_number",
    ]
