from wtforms import TextAreaField
from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import format_as_markup
from calendarapi.commons.exeptions import URL_FORMAT
from calendarapi.models import Contact


CONTACT_LEN = Contact.value.type.length


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
    form_args = {"value": {"description": URL_FORMAT % CONTACT_LEN}}
    column_formatters = {
        "value": format_as_markup,
    }

    def on_form_prefill(self, form, id):
        if form._obj.contact_type in ["phone", "mail"]:
            form.value.description = None
        return super().on_form_prefill(form, id)
