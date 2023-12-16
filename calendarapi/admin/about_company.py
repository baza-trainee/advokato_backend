import os

from flask import request, current_app
from markupsafe import Markup
from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

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


class AboutCompanyModelView(AdminModelView):
    can_set_page_size = True
    column_labels = {
        "main_page_photo_path": "Фото(головна)",
        "our_team_page_photo_path": "Фото(про компанію)",
        "main_page_description": "Опис(головна)",
        "our_team_page_description": "Опис(про компанію)",
    }
    column_list = [
        "main_page_photo_path",
        "our_team_page_photo_path",
        "main_page_description",
        "our_team_page_description",
    ]
    form_columns = [
        "main_page_description",
        "our_team_page_description",
        "main_page_photo_path",
        "our_team_page_photo_path",
    ]
    column_descriptions = {
        "main_page_photo_path": """Відображається на головній сторінці. Розмір до 30 мб, формати: PNG, JPG, JPEG, WebP""",
        "our_team_page_photo_path": """Відображається на сторінці "Про компанію". Розмір до 30 мб, формати: PNG, JPG, JPEG, WebP""",
        "main_page_description": """Відображається на головній сторінці під блоком Hero, максимальна кількість символів - 500.""",
        "our_team_page_description": """Відображається на сторінці "Про компанію". Ви можете використовувати HTML-теги, щоб зробити абзац, створити список і т. д., для покращення зручності читання. Максимальна кількість символів - 3000""",
    }

    can_create = False
    can_delete = False

    column_formatters = {
        "main_page_photo_path": thumbnail_formatter(field_name="main_page_photo_path"),
        "our_team_page_photo_path": thumbnail_formatter(field_name="our_team_page_photo_path"),
        "our_team_page_description": format_text_as_markup,
        "main_page_description": format_text_as_markup,
    }

    form_extra_fields = {
        "our_team_page_photo_path": FileField(
            """Виберіть фото для сторінки "Наша компанія".""",
            validators=[validate_image()],
            description="Розмір до 30 мб, формати: PNG, JPG, JPEG, WebP."
        ),
        "our_team_page_description": TextAreaField(
            """Опис для сторінки "Наша компанія". """,
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message="Це поле обов'язкове.")],
            description="До 3000 символів."
        ),
        "main_page_photo_path": FileField(
            "Виберіть фото для головної сторінки.",
            validators=[validate_image()],
            description="Розмір до 30 мб, формати: PNG, JPG, JPEG, WebP."
        ),
        "main_page_description": TextAreaField(
            "Короткий опис для головної сторінки. ",
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message="Це поле обов'язкове.")],
            description="До 500 символів."
        ),
    }

    def on_model_delete(self, model):
        if model.main_page_photo_path:
            custom_delete_file(ABS_MEDIA_PATH, model.main_page_photo_path)
        if model.our_team_page_photo_path:
            custom_delete_file(ABS_MEDIA_PATH, model.our_team_page_photo_path)
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        if model.main_page_photo_path:
            if form.main_page_photo_path.object_data:
                custom_delete_file(ABS_MEDIA_PATH, form.main_page_photo_path.object_data)
            model.main_page_photo_path = custom_save_file(ABS_MEDIA_PATH, model.main_page_photo_path)
        else:
            model.main_page_photo_path = form.main_page_photo_path.object_data

        if model.our_team_page_photo_path:
            if form.our_team_page_photo_path.object_data:
                custom_delete_file(ABS_MEDIA_PATH, form.our_team_page_photo_path.object_data)
            model.our_team_page_photo_path = custom_save_file(
                ABS_MEDIA_PATH, model.our_team_page_photo_path
            )
        else:
            model.our_team_page_photo_path = form.our_team_page_photo_path.object_data
        return super().on_model_change(form, model, is_created)