from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter
from calendarapi.admin.commons.validators import ImageValidator, validate_text
from calendarapi.commons.exeptions import (
    DATA_REQUIRED,
    REQ_IMAGE,
    REQ_IMAGE_RESOLUTION,
    REQ_MAX_LEN,
)
from calendarapi.commons.utils import custom_delete_file, custom_update_file
from calendarapi.models.reviews import Reviews


NAME_LEN = Reviews.name.type.length
POSITION_LEN = Reviews.position.type.length
DESCRIPTION_LEN = Reviews.description.type.length
REQ_PHOTO_PATH = REQ_IMAGE_RESOLUTION % (240, 240)


class ReviewsModelView(AdminModelView):
    can_set_page_size = True

    column_labels = {
        "name": "Ім'я Прізвище",
        "position": "Посада",
        "description": "Опис",
        "photo_path": "Фото",
        "created_at": "Дата",
    }
    column_sortable_list = [
        "created_at",
    ]
    column_searchable_list = [
        "name",
    ]
    column_default_sort = [
        ("id", False),
    ]
    column_list = [
        "photo_path",
        "name",
        "position",
        "description",
        "created_at",
    ]

    column_formatters = {
        "photo_path": ThumbnailFormatter(width=80),
    }

    form_extra_fields = {
        "photo_path": FileField(
            label="Виберіть фото для відгуку",
            validators=[ImageValidator()],
            description=f"{REQ_IMAGE} {REQ_PHOTO_PATH}",
        ),
        "description": TextAreaField(
            label="Опис",
            render_kw={
                "class": "form-control",
                "rows": 5,
                "maxlength": DESCRIPTION_LEN,
            },
            validators=[DataRequired(message=DATA_REQUIRED), validate_text],
            description=REQ_MAX_LEN % DESCRIPTION_LEN,
        ),
    }

    form_args = {
        "created_at": {
            "validators": [DataRequired(message=DATA_REQUIRED)],
        },
        "name": {"description": REQ_MAX_LEN % NAME_LEN},
        "position": {"description": REQ_MAX_LEN % POSITION_LEN},
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        return super().on_model_change(form, model, is_created)
