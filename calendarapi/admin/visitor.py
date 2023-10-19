from calendarapi.admin.common import AdminModelView


class VisitorModelView(AdminModelView):
    can_set_page_size = True
    can_create = False
    can_edit = True
    can_export = True
    export_types = [
        "csv",
        "xls",
        "xlsx",
        "json",
        "yaml",
        "html",
    ]

    column_labels = {
        "id": "ID Клієнта",
        "name": "ім'я",
        "surname": "Прізвище",
        "phone_number": "Мобільний",
        "email": "Пошта",
    }

    # column_sortable_list = [
    #     "lawyers.name",
    # ]

    # column_searchable_list = [
    #     "lawyers.name",
    #     "lawyers.surname",
    # ]
