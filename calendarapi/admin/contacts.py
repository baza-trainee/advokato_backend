from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import format_as_markup
from calendarapi.commons.exeptions import REQ_MAX_LEN


class ContactModelView(AdminModelView):
    can_set_page_size = True
    can_create = False
    can_delete = False
    can_edit = True
    column_sortable_list = []
    column_default_sort = [
        ("id", False),
    ]
    column_labels = {
        "contact_type": "Контакт",
        "value": "Значення",
    }
    column_list = [
        "contact_type",
        "value",
    ]
    form_columns = [
        "value",
    ]
    form_args = {"value": {"description": REQ_MAX_LEN % 500}}
    column_formatters = {
        "value": format_as_markup,
    }
