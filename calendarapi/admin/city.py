from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import format_as_markup


class CityModelView(AdminModelView):
    form_excluded_columns = ["lawyers"]

    column_default_sort = [
        ("id", False),
    ]

    column_labels = {
        "city_name": "Місто",
        "address": "Адреса філіалу",
    }

    column_list = [
        "city_name",
        "address",
    ]

    column_formatters = {
        "address": format_as_markup,
    }

    column_sortable_list = []

    column_descriptions = {
        "address": "Адреси відображатимуться на сайті, в розділі 'контакти'.",
    }
