from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter, format_as_markup
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.exeptions import (
    DATA_REQUIRED,
    REQ_IMAGE,
    REQ_MAX_LEN,
    REQ_HTML_M,
)
from calendarapi.commons.utils import custom_delete_file, custom_update_file
from calendarapi.models.pro_bono import ProBono


DESCRIPTION_LEN = ProBono.description.type.length


class ProBonoModelView(AdminModelView):
    can_set_page_size = True
    column_labels = {
        "photo_path": "Фото",
        "description": "Опис",
    }

    form_columns = [
        "description",
        "photo_path",
    ]

    column_formatters = {
        "photo_path": ThumbnailFormatter(),
        "description": format_as_markup,
    }

    column_default_sort = [
        ("id", False),
    ]

    form_extra_fields = {
        "photo_path": FileField(
            label="Виберіть фото партнера",
            validators=[ImageValidator()],
            description=REQ_IMAGE,
        ),
        "description": TextAreaField(
            label="Опис",
            render_kw={
                "class": "form-control",
                "rows": 5,
                "maxlength": DESCRIPTION_LEN,
            },
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=f"{REQ_MAX_LEN % DESCRIPTION_LEN} {REQ_HTML_M}",
        ),
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        return super().on_model_change(form, model, is_created)
