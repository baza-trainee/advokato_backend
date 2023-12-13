import os

from flask import request, current_app
from markupsafe import Markup
from wtforms.validators import DataRequired
from wtforms import BooleanField, TextAreaField, FileField, ValidationError
from flask_admin.form import rules
from calendarapi.admin.common import (
    AdminModelView,
    get_media_path,
    custom_delete_file,
    custom_save_file,
)

ABS_MEDIA_PATH = get_media_path(__name__.split(".")[-1])


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
        "photo_path": """Фото для сторінки "Наша команда".""",
        "slider_photo_path": """Фото для слайдеру на головній сторінці. Якщо залишити це поле пустим, відповідний спеціаліст не відображатиметься в слайдері.""",
        "description": """Ви можете використовувати HTML-теги, щоб зробити абзац, створити список і т. д., для покращення зручності читання.""",
    }
    form_rules = [
        "name",
        "position",
        "description",
        "photo_path",
        rules.FieldSet(
            [
                "slider_photo_path",
                "delete_slider_photo",  # Checkbox to delete the slider photo
            ]
        ),
    ]

    def _format_description(view, context, model, name):
        return Markup(f'<div style="text-align: left">{model.description}</div>')

    def _list_thumbnail(width: int = 240):
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            if current_app.config["STORAGE"] == "STATIC":
                url = os.path.join(request.host_url, model.photo_path)
            else:
                url = model.photo_path

            if model.photo_path.split(".")[-1] in current_app.config["IMAGE_FORMATS"]:
                return Markup(f"<img src={url} width={width}>")

        return thumbnail_formatter

    def _list_thumbnail(width: int = 240, field_name: str = "photo_path"):
        def thumbnail_formatter(view, context, model, name):
            field_value = getattr(model, field_name)
            if not field_value:
                return ""

            if current_app.config["STORAGE"] == "STATIC":
                url = os.path.join(request.host_url, field_value)
            else:
                url = field_value

            if field_value.split(".")[-1] in current_app.config["IMAGE_FORMATS"]:
                return Markup(f"<img src={url} width={width}>")

        return thumbnail_formatter

    column_formatters = {
        "photo_path": _list_thumbnail(field_name="photo_path"),
        "slider_photo_path": _list_thumbnail(field_name="slider_photo_path"),
        "description": _format_description,
    }

    def _custom_validate_media(form, field):
        if not form.photo_path.object_data and not form.photo_path.data:
            raise ValidationError("Це поле обов'язкове.")

    form_extra_fields = {
        "photo_path": FileField(
            "Виберіть фото партнера",
            validators=[_custom_validate_media],
        ),
        "slider_photo_path": FileField("Виберіть фото партнера для слайдеру."),
        "description": TextAreaField(
            "Опис",
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message="Це поле обов'язкове.")],
        ),
        "delete_slider_photo": BooleanField("Видалити фото зі слайдеру"),
    }

    def on_model_delete(self, model):
        if model.photo_path:
            custom_delete_file(ABS_MEDIA_PATH, model.photo_path)
        if model.slider_photo_path:
            custom_delete_file(ABS_MEDIA_PATH, model.slider_photo_path)
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        if model.photo_path:
            if form.photo_path.object_data:
                custom_delete_file(ABS_MEDIA_PATH, form.photo_path.object_data)
            model.photo_path = custom_save_file(ABS_MEDIA_PATH, model.photo_path)
        else:
            model.photo_path = form.photo_path.object_data

        if model.slider_photo_path:
            if form.slider_photo_path.object_data:
                custom_delete_file(ABS_MEDIA_PATH, form.slider_photo_path.object_data)
            model.slider_photo_path = custom_save_file(
                ABS_MEDIA_PATH, model.slider_photo_path
            )
        else:
            model.slider_photo_path = form.slider_photo_path.object_data

        if form.delete_slider_photo.data and model.slider_photo_path:
            custom_delete_file(ABS_MEDIA_PATH, model.slider_photo_path)
            model.slider_photo_path = None
        return super().on_model_change(form, model, is_created)
