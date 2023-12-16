import os

from flask import request, current_app
from markupsafe import Markup
from wtforms.validators import DataRequired
from wtforms import BooleanField, TextAreaField, FileField, ValidationError
from flask_admin.form import rules
from calendarapi.admin.common import (
    AdminModelView,
    format_text_as_markup,
    get_media_path,
    custom_delete_file,
    custom_save_file,
    thumbnail_formatter,
    validate_image,
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
        "slider_photo_path": """Фото для слайдеру на головній сторінці. Якщо залишити це поле пустим, відповідний спеціаліст не відображатиметься у слайдері.""",
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

    column_formatters = {
        "photo_path": thumbnail_formatter(field_name="photo_path"),
        "slider_photo_path": thumbnail_formatter(field_name="slider_photo_path"),
        "description": format_text_as_markup,
    }

    form_extra_fields = {
        "photo_path": FileField(
            "Виберіть фото партнера",
            validators=[validate_image()],
        ),
        "slider_photo_path": FileField(
            "Виберіть фото партнера для слайдеру.",
            validators=[validate_image(required=False)],
        ),
        "description": TextAreaField(
            "Опис",
            validators=[DataRequired(message="Це поле обов'язкове.")],
            render_kw={"class": "form-control", "rows": 5, "maxlength": 3000},
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
            if form.slider_photo_path.object_data or form.delete_slider_photo.data:
                custom_delete_file(ABS_MEDIA_PATH, form.slider_photo_path.object_data)
            if form.delete_slider_photo.data:
                model.slider_photo_path = None
            else:
                model.slider_photo_path = custom_save_file(
                    ABS_MEDIA_PATH, model.slider_photo_path
                )
        else:
            model.slider_photo_path = form.slider_photo_path.object_data

        return super().on_model_change(form, model, is_created)

    # def on_form_prefill(self, form, id):
    #     if not form.slider_photo_path.object_data:
    #         del form._fields["delete_slider_photo"]
    #     return super().on_form_prefill(form, id)
