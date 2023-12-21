from datetime import datetime
from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter, format_as_markup
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.exeptions import (
    DATA_REQUIRED,
    REQ_HTML_M,
    REQ_IMAGE,
    REQ_MAX_LEN,
)
from calendarapi.commons.utils import custom_delete_file, custom_update_file
from calendarapi.models import News


NAME_LEN = News.name.type.length
DESCRIPTION_LEN = News.description.type.length


class NewsModelView(AdminModelView):
    can_set_page_size = True
    column_sortable_list = [
        "created_at",
    ]
    column_searchable_list = [
        "name",
    ]
    column_default_sort = [
        ("id", False),
    ]

    column_labels = {
        "name": "Новина",
        "description": "Опис",
        "created_at": "Дата",
        "photo_path": "Фото",
    }

    column_list = [
        "photo_path",
        "name",
        "description",
        "created_at",
    ]

    column_formatters = {
        "description": format_as_markup,
        "photo_path": ThumbnailFormatter(),
        "created_at": lambda view, context, model, name: model.created_at.strftime(
            "%d/%m/%Y, %H:%M"
        ),
    }

    form_extra_fields = {
        "photo_path": FileField(
            label="Виберіть фото для новини",
            validators=[ImageValidator()],
            description=REQ_IMAGE,
        ),
        "description": TextAreaField(
            label="Опис",
            render_kw={"class": "form-control", "rows": 5, "maxlength": DESCRIPTION_LEN},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=f"{REQ_MAX_LEN % DESCRIPTION_LEN} {REQ_HTML_M}",
        ),
    }

    form_args = {
        "name": {"description": REQ_MAX_LEN % NAME_LEN},
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        return super().on_model_change(form, model, is_created)
