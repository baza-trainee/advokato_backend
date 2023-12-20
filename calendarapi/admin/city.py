from markupsafe import Markup
from wtforms import StringField, ValidationError

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import format_as_markup
from calendarapi.commons.exeptions import IVNALID_COORDS, REQ_MAX_LEN

ADDRESS_INFO = "Адреси відображатимуться на сайті, в розділі 'контакти'."
COORDS_INFO = "Необхідні для відображення міток на карті"


def validate_float(form, field):
    try:
        field.data = field.data.strip().replace(",", ".")
        float(field.data)
    except Exception:
        raise ValidationError(message=IVNALID_COORDS)


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
    column_sortable_list = []
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
    column_descriptions = {
        "address": ADDRESS_INFO,
        "coordinates": COORDS_INFO,
    }

    form_extra_fields = {
        "latitude": StringField(
            "Координати (Широта)", validators=[validate_float], description=COORDS_INFO
        ),
        "longitude": StringField(
            "Координати (Довгота)", validators=[validate_float], description=COORDS_INFO
        ),
    }
    form_args = {
        "city_name": {
            "description": REQ_MAX_LEN % 100,
        },
        "address": {
            "description": f"{ADDRESS_INFO} {REQ_MAX_LEN % 200}",
        },
    }
