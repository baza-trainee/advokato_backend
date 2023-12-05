from markupsafe import Markup

from calendarapi.admin.common import AdminModelView


class ContactModelView(AdminModelView):
    can_set_page_size = True
    column_labels = {
        "contact_type": "Контакт",
        "value": "Значення",
    }

    column_default_sort = [
        ("id", False),
    ]
    column_list = [
        "contact_type",
        "value",
    ]
    form_columns = [
        "value",
    ]

    def _format_description(view, context, model, name):
        return Markup(model.value)

    column_formatters = {
        "value": _format_description,
    }
    can_create = False
    can_delete = False
    can_edit = True
    column_sortable_list = []
