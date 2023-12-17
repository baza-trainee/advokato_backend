from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter, format_as_markup
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.exeptions import DATA_REQUIRED
from calendarapi.commons.utils import custom_delete_file, custom_update_file


class AboutCompanyModelView(AdminModelView):
    can_set_page_size = True
    can_create = False
    can_delete = False

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

    column_formatters = {
        "main_page_photo_path": ThumbnailFormatter(),
        "our_team_page_photo_path": ThumbnailFormatter(),
        "our_team_page_description": format_as_markup,
        "main_page_description": format_as_markup,
    }

    form_extra_fields = {
        "our_team_page_photo_path": FileField(
            """Виберіть фото для сторінки "Наша компанія".""",
            validators=[ImageValidator()],
            description="Розмір до 30 мб, формати: PNG, JPG, JPEG, WebP.",
        ),
        "our_team_page_description": TextAreaField(
            """Опис для сторінки "Наша компанія". """,
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description="До 3000 символів.",
        ),
        "main_page_photo_path": FileField(
            label="Виберіть фото для головної сторінки.",
            validators=[ImageValidator()],
            description="Розмір до 30 мб, формати: PNG, JPG, JPEG, WebP.",
        ),
        "main_page_description": TextAreaField(
            label="Короткий опис для головної сторінки. ",
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description="До 500 символів.",
        ),
    }

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="main_page_photo_path")
        custom_update_file(model, form, field_name="our_team_page_photo_path")
        return super().on_model_change(form, model, is_created)
