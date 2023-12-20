from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter, format_as_markup
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.exeptions import DATA_REQUIRED, REQ_MAX_LEN
from calendarapi.commons.utils import custom_delete_file, custom_update_file

DESCRIPTION_INFO = "Відображається зліва або справа від фото."
TITLE_INFO = "Заголовок під фото."
SHORT_TEXT_INFO = "Текст який буде під заголовком, накладений на фото."


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
        "title": TITLE_INFO,
        "short_text": SHORT_TEXT_INFO,
        "description": DESCRIPTION_INFO,
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
            render_kw={"class": "form-control", "rows": 5, "maxlength": 500},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=f"{DESCRIPTION_INFO} {REQ_MAX_LEN % 500}",
        ),
    }
    form_args = {
        "title": {
            "description": f"{TITLE_INFO} {REQ_MAX_LEN % 100}",
        },
        "short_text": {
            "description": f"{SHORT_TEXT_INFO} {REQ_MAX_LEN % 300}",
        },
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        return super().on_model_change(form, model, is_created)
