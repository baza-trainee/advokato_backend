from markupsafe import Markup
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import format_as_markup
from calendarapi.commons.exeptions import IVNALID_COORDS, REQ_MAX_LEN, DATA_REQUIRED
from calendarapi.models import City

ADDRESS_INFO = "Адреси відображатимуться на сайті, в розділі 'контакти'."
COORDS_INFO = "Необхідні для відображення міток на карті"
CITY_NAME_LEN = City.city_name.type.length
CITY_ADDRESS_LEN = City.address.type.length


def validate_coord(form, field):
    """>=0 <=0 and int/float"""
    try:
        field.data = field.data.strip().replace(",", ".")
        data = float(field.data)
        if not (data < 0 or data > 0):
            field.data = data
            raise ValueError()
    except Exception:
        raise ValidationError(message=IVNALID_COORDS)


def format_coords(view, context, model, name):
    res = '<div style="display: flex;">'
    coords = {"Широта": model.latitude, "Довгота": model.longitude}
    for coord_name, coord in coords.items():
        # formatted_coord = "{:.100f}".format(coord) # higth accuracy
        res += f'<div class="city_coordinates">'
        res += f'<span class="city_coord_name"> {coord_name}:</span><span class="city_coord_value">{coord}</span>'
        res += "</div>"
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
            "Координати (Широта)",
            validators=[DataRequired(message=DATA_REQUIRED), validate_coord],
            description=COORDS_INFO,
        ),
        "longitude": StringField(
            "Координати (Довгота)",
            validators=[DataRequired(message=DATA_REQUIRED), validate_coord],
            description=COORDS_INFO,
        ),
    }
    form_args = {
        "city_name": {
            "description": REQ_MAX_LEN % CITY_NAME_LEN,
        },
        "address": {
            "description": f"{ADDRESS_INFO} {REQ_MAX_LEN % CITY_ADDRESS_LEN}",
        },
    }
