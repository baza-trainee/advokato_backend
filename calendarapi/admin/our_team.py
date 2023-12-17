import os

from wtforms.validators import DataRequired
from wtforms import BooleanField, TextAreaField, FileField
from wtforms.widgets import CheckboxInput
from flask_admin.form import rules

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter, format_as_markup
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.utils import custom_delete_file, custom_update_file


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
        "slider_photo_path": """Фото для слайдеру на головній сторінці. Якщо залишити це поле пустим,
відповідний спеціаліст не відображатиметься у слайдері.""",
        "description": """Ви можете використовувати HTML-теги, щоб зробити абзац, створити список і т. д.,
для покращення зручності читання.""",
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
        "photo_path": ThumbnailFormatter(),
        "slider_photo_path": ThumbnailFormatter(),
        "description": format_as_markup,
    }

    form_extra_fields = {
        "photo_path": FileField(
            label="Виберіть фото партнера",
            validators=[ImageValidator()],
        ),
        "slider_photo_path": FileField(
            label="Виберіть фото партнера для слайдеру.",
            validators=[ImageValidator(required=False)],
        ),
        "description": TextAreaField(
            label="Опис",
            validators=[DataRequired(message="Це поле обов'язкове.")],
            render_kw={"class": "form-control", "rows": 5, "maxlength": 3000},
        ),
        "delete_slider_photo": BooleanField("Видалити фото зі слайдеру"),
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="photo_path")
        custom_delete_file(model, field_name="slider_photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        custom_update_file(model, form, field_name="slider_photo_path")

        if form.delete_slider_photo.data:
            custom_delete_file(model, field_name="slider_photo_path")
            model.slider_photo_path = None

        return super().on_model_change(form, model, is_created)

    # def on_form_prefill(self, form, id):
    #     if not id:
    #         del form._fields["delete_slider_photo"]
    #     self.form_rules
    #     return super().on_form_prefill(form, id)
