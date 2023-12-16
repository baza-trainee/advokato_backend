from markupsafe import Markup

from calendarapi.admin.common import AdminModelView


class CityModelView(AdminModelView):
    form_excluded_columns = ["lawyers"]

    column_labels = {"city_name": "Місто", "address": "Адреса філіалу"}

    column_list = ["city_name", "address"]

    column_default_sort = [
        ("id", False),
    ]

    def _format_description(view, context, model, name):
        return Markup(model.address)

    column_formatters = {
        "address": _format_description,
    }

    column_sortable_list = []

    column_descriptions = {
        "address": "Адреси відображатимуться на сайті, в розділі 'контакти'."
    }
