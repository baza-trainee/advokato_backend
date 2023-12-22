from wtforms.validators import DataRequired
from wtforms import BooleanField, TextAreaField, FileField

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
from calendarapi.models import OurTeam


PHOTO_PATH_INFO = 'Фото для сторінки "Наша команда".'
SLIDER_PHOTO_PATH_INFO = """Фото для слайдеру на головній сторінці. Якщо залишити це поле пустим,
відповідний спеціаліст не відображатиметься у слайдері."""
NAME_LEN = OurTeam.name.type.length
POSITION_LEN = OurTeam.position.type.length
DESCRIPTION_LEN = OurTeam.description.type.length


class OurTeamModelView(AdminModelView):
    can_set_page_size = True
    column_labels = {
        "photo_path": "Фото",
        "slider_photo_path": "Слайдер",
        "name": "Ім'я",
        "position": "Посада",
        "description": "Опис",
    }
    column_sortable_list = [
        "name",
    ]
    column_searchable_list = [
        "name",
    ]
    column_default_sort = [
        ("id", False),
    ]
    column_list = [
        "photo_path",
        "slider_photo_path",
        "name",
        "position",
        "description",
    ]
    form_columns = [
        "name",
        "position",
        "description",
        "photo_path",
        "slider_photo_path",
        "delete_slider_photo",
    ]
    column_descriptions = {
        "photo_path": PHOTO_PATH_INFO,
        "slider_photo_path": SLIDER_PHOTO_PATH_INFO,
    }

    column_formatters = {
        "photo_path": ThumbnailFormatter(),
        "slider_photo_path": ThumbnailFormatter(),
        "description": format_as_markup,
    }

    form_extra_fields = {
        "photo_path": FileField(
            label="Виберіть фото партнера",
            validators=[ImageValidator()],
            description=REQ_IMAGE,
        ),
        "slider_photo_path": FileField(
            label="Виберіть фото партнера для слайдеру.",
            validators=[ImageValidator(required=False)],
            description=f"{SLIDER_PHOTO_PATH_INFO} {REQ_IMAGE}",
        ),
        "description": TextAreaField(
            label="Опис",
            validators=[DataRequired(message=DATA_REQUIRED)],
            render_kw={
                "class": "form-control",
                "rows": 5,
                "maxlength": DESCRIPTION_LEN,
            },
            description=f"{REQ_MAX_LEN % DESCRIPTION_LEN} {REQ_HTML_M}",
        ),
        "delete_slider_photo": BooleanField("Видалити фото зі слайдеру"),
    }
    form_args = {
        "name": {
            "description": REQ_MAX_LEN % NAME_LEN,
        },
        "position": {
            "description": REQ_MAX_LEN % POSITION_LEN,
        },
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="photo_path")
        custom_delete_file(model, field_name="slider_photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        custom_update_file(model, form, field_name="slider_photo_path")

        if form.delete_slider_photo and form.delete_slider_photo.data:
            custom_delete_file(model, field_name="slider_photo_path")
            model.slider_photo_path = None

        return super().on_model_change(form, model, is_created)

    def on_form_prefill(self, form, id):
        if not form.slider_photo_path.data:
            del form.delete_slider_photo
        return super().on_form_prefill(form, id)

    def create_form(self, obj=None):
        form = super().create_form(obj)
        del form.delete_slider_photo
        return form
