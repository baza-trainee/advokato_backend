from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter, format_as_markup
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.exeptions import DATA_REQUIRED, REQ_HTML_M, REQ_MAX_LEN
from calendarapi.commons.utils import custom_delete_file, custom_update_file

SPECIALIZATION_DESCRIPTION_FULL_INFO = """Доповнення до опису. Відображається при натисканні на кнопку "Детальніше" 
при перегляді практик."""


class SpecializationModelView(AdminModelView):
    form_excluded_columns = ["lawyers"]
    column_list = [
        "specialization_photo",
        "specialization_name",
        "specialization_description",
        "specialization_description_full",
    ]

    column_default_sort = [
        ("id", False),
    ]

    column_labels = {
        "specialization_photo": "Фото",
        "specialization_name": "Спеціалізація",
        "specialization_description": "Опис",
        "specialization_description_full": "Детальніше",
    }

    form_args = {
        "specialization_name": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        }
    }

    form_columns = [
        "specialization_name",
        "specialization_description",
        "specialization_description_full",
        "specialization_photo",
    ]
    column_descriptions = {
        "specialization_description_full": SPECIALIZATION_DESCRIPTION_FULL_INFO
    }

    column_formatters = {
        "specialization_photo": ThumbnailFormatter(),
        "specialization_description_full": format_as_markup,
    }

    form_extra_fields = {
        "specialization_photo": FileField(
            label="Виберіть фото для спеціалізації",
            validators=[ImageValidator()],
        ),
        "specialization_description": TextAreaField(
            label="Опис",
            render_kw={"class": "form-control", "rows": 5, "maxlength": 1000},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=f"{REQ_MAX_LEN % 1000} {REQ_HTML_M}",
        ),
        "specialization_description_full": TextAreaField(
            label="Детальніше",
            render_kw={"class": "form-control", "rows": 5, "maxlength": 3000},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=f"{SPECIALIZATION_DESCRIPTION_FULL_INFO} {REQ_MAX_LEN % 3000} {REQ_HTML_M}",
        ),
    }
    form_args = {
        "specialization_name": {
            "description": f"{REQ_MAX_LEN % 255}",
        },
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="specialization_photo")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="specialization_photo")
        return super().on_model_change(form, model, is_created)
