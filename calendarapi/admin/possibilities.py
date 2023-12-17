from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter, format_as_markup
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.exeptions import DATA_REQUIRED
from calendarapi.commons.utils import custom_delete_file, custom_update_file


class PossibilitiesModelView(AdminModelView):
    can_set_page_size = True
    column_labels = {
        "photo_path": "Фото",
        "title": "Гасло",
        "short_text": "Короткий опис",
        "description": "Опис",
    }
    column_default_sort = [
        ("id", False),
    ]
    column_list = [
        "photo_path",
        "title",
        "short_text",
        "description",
    ]
    form_columns = [
        "title",
        "short_text",
        "description",
        "photo_path",
    ]
    column_descriptions = {
        "title": "Заголовок під фото.",
        "short_text": "Текст який буде під заголовком, накладений на фото.",
        "description": "Відображається зліва або справа від фото.",
    }

    column_formatters = {
        "photo_path": ThumbnailFormatter(),
        "description": format_as_markup,
    }

    form_extra_fields = {
        "photo_path": FileField(
            label="Виберіть фото.",
            validators=[ImageValidator()],
        ),
        "description": TextAreaField(
            label="Опис",
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message=DATA_REQUIRED)],
        ),
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        return super().on_model_change(form, model, is_created)
