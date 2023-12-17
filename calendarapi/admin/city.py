from markupsafe import Markup
from wtforms import StringField, ValidationError
from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import format_as_markup


def validate_float(form, field):
    try:
        field.data = field.data.strip().replace(",", ".")
        float(field.data)
    except Exception as exc:
        raise ValidationError(
            "Невірний формат для координат. Приймаються лише дробові та цілі числа."
        )


def format_coords(view, context, model, name):
    res = '<div class="city_coordinates">'
    coords = [model.latitude, model.longitude]
    if all(coords):
        res += f'<span class="city_coord_name"> Широта:</span><span class="city_coord_value">{model.latitude}</span>'
        res += f'<span class="city_coord_name"> Довгота:</span><span class="city_coord_value">{model.longitude}</span>'
    res += "</div>"
    return Markup(res)


class CityModelView(AdminModelView):
    form_excluded_columns = ["lawyers"]

    column_default_sort = [
        ("id", False),
    ]

    column_labels = {
        "city_name": "Місто",
        "address": "Адреса філіалу",
        "coordinates": "Координати",
    }

    column_list = [
        "city_name",
        "address",
        "coordinates",
    ]

    column_formatters = {
        "address": format_as_markup,
        "coordinates": format_coords,
    }
    form_extra_fields = {
        "latitude": StringField("Координати (Широта)", validators=[validate_float]),
        "longitude": StringField("Координати (Довгота)", validators=[validate_float]),
    }

    column_sortable_list = []

    column_descriptions = {
        "address": "Адреси відображатимуться на сайті, в розділі 'контакти'.",
    }
