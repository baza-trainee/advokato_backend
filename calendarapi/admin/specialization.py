import os
from flask import current_app, request

from markupsafe import Markup
from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField, ValidationError

from calendarapi.admin.common import (
    AdminModelView,
    get_media_path,
    custom_delete_file,
    custom_save_file,
)

ABS_MEDIA_PATH = get_media_path(__name__.split(".")[-1])


class SpecializationAdminModelView(AdminModelView):
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
        },
        "specialization_description": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        },
        "specialization_description_full": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        },
        "specialization_photo": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        },
    }

    form_columns = [
        "specialization_name",
        "specialization_description",
        "specialization_description_full",
        "specialization_photo",
    ]
    column_descriptions = {
        "specialization_description_full": """Доповнення до опису. Відображається при натисканні на кнопку "Детальніше" при перегляді практик."""
    }

    def _format_description(view, context, model, name):
        return Markup(model.specialization_description_full)

    def _list_thumbnail(width: int = 240):
        def thumbnail_formatter(view, context, model, name):
            if not model.specialization_photo:
                return ""
            if current_app.config["STORAGE"] == "STATIC":
                url = os.path.join(request.host_url, model.specialization_photo)
            else:
                url = model.specialization_photo

            if (
                model.specialization_photo.split(".")[-1]
                in current_app.config["IMAGE_FORMATS"]
            ):
                return Markup(f"<img src={url} width={width}>")

        return thumbnail_formatter

    column_formatters = {
        "specialization_photo": _list_thumbnail(),
        "specialization_description_full": _format_description,
    }

    def _custom_validate_media(form, field):
        if (
            not form.specialization_photo.object_data
            and not form.specialization_photo.data
        ):
            raise ValidationError("Це поле обов'язкове.")

    form_extra_fields = {
        "specialization_photo": FileField(
            "Виберіть фото для спеціалізації",
            validators=[_custom_validate_media],
        ),
        "specialization_description": TextAreaField(
            "Опис",
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message="Це поле обов'язкове.")],
        ),
        "specialization_description_full": TextAreaField(
            "Детальніше",
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message="Це поле обов'язкове.")],
        ),
    }

    def on_model_delete(self, model):
        custom_delete_file(ABS_MEDIA_PATH, model.specialization_photo)
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        if model.specialization_photo:
            if form.specialization_photo.object_data:
                custom_delete_file(
                    ABS_MEDIA_PATH, form.specialization_photo.object_data
                )
            model.specialization_photo = custom_save_file(
                ABS_MEDIA_PATH, model.specialization_photo
            )
        else:
            model.specialization_photo = form.specialization_photo.object_data
        return super().on_model_change(form, model, is_created)
