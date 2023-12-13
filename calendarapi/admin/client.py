import os

from wtforms.validators import DataRequired
from flask import current_app, request
from markupsafe import Markup
from wtforms import TextAreaField, ValidationError
from wtforms import FileField

from calendarapi.admin.common import (
    AdminModelView,
    get_media_path,
    custom_delete_file,
    custom_save_file,
)

ABS_MEDIA_PATH = get_media_path(__name__.split(".")[-1])


class ClientsAdminModelView(AdminModelView):
    can_set_page_size = True

    column_labels = {
        "photo_path": "Фото",
        "link": "Посилання",
    }

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

    column_formatters = {
        "photo_path": _list_thumbnail(),
    }

    def _custom_validate_media(form, field):
        if not form.photo_path.object_data and not form.photo_path.data:
            raise ValidationError("Це поле обов'язкове.")

    form_extra_fields = {
        "photo_path": FileField(
            "Виберіть фото для новини",
            validators=[_custom_validate_media],
        ),
    }

    def on_model_delete(self, model):
        custom_delete_file(ABS_MEDIA_PATH, model.photo_path)
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        if model.photo_path:
            if form.photo_path.object_data:
                custom_delete_file(ABS_MEDIA_PATH, form.photo_path.object_data)
            model.photo_path = custom_save_file(ABS_MEDIA_PATH, model.photo_path)
        else:
            model.photo_path = form.photo_path.object_data
        return super().on_model_change(form, model, is_created)
