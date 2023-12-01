import os
import uuid
from flask import request
from markupsafe import Markup
from calendarapi.admin.common import AdminModelView
from flask_admin import form
from wtforms import TextAreaField
from cloudinary import uploader
from wtforms import FileField

file_path = os.path.abspath(os.path.dirname(__name__))
our_team_dir = os.path.join(file_path, "calendarapi", "static", "media", "team")


class OurTeamModelView(AdminModelView):
    can_set_page_size = True
    column_labels = {
        "photo_path": "Фото",
        "name": "Ім'я",
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
        "name",
        "description",
    ]
    form_columns = [
        "name",
        "description",
        "photo_path",
    ]
    column_descriptions = {
        "description": """Ви можете використовувати HTML-теги, щоб логічно розділити текст на блоки, створити список і т. д., для покращення зручності читання."""
    }

    def _format_description(view, context, model, name):
        return Markup(model.description)

    def _list_thumbnail():
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            # url = os.path.join(request.host_url, "static", "media", "team", model.photo_path)
            url = model.photo_path
            if model.photo_path.split(".")[-1] in [
                "jpg",
                "jpeg",
                "png",
                "svg",
                "gif",
                "webp",
            ]:
                return Markup(f"<img src={url} width=240>")

        return thumbnail_formatter

    column_formatters = {
        "photo_path": _list_thumbnail(),
        "description": _format_description,
    }

    # def generate_image_name(model, file_data):
    #     return f'{uuid.uuid4().hex[:16]}.{file_data.filename.split(".")[-1]}'

    # def validate_directory(form, field):
    #     upload_folder = os.path.join(file_path, "calendarapi", "static", "media", "team")
    #     os.makedirs(upload_folder, exist_ok=True)

    form_extra_fields = {
        "photo_path": FileField("Виберіть фото партнера"),
        # "photo_path": form.ImageUploadField(
        #     "Виберіть фото партнера",
        #     base_path=os.path.join(file_path, "calendarapi", "static", "media", "team"),
        #     url_relative_path=os.path.join('media', 'team', ''),
        #     namegen=generate_image_name,
        #     allowed_extensions=["jpg", "png", "jpeg", "gif", "webp", "svg"],
        #     validators=[validate_directory],
        # ),
        "description": TextAreaField(
            "Опис", render_kw={"class": "form-control", "rows": 3}
        ),
    }

    # def on_model_delete(self, model):
    #     file_path = f"{our_team_dir}/{model.photo_path}"
    #     if os.path.exists(file_path):
    #         os.remove(file_path)
    #     return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        if model.photo_path:
            upload_result = uploader.upload(model.photo_path)
            model.photo_path = upload_result["url"]
        else:
            model.photo_path = form.photo_path.object_data
        return super().on_model_change(form, model, is_created)
