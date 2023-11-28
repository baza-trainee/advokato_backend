import os
import uuid
from flask import url_for
from markupsafe import Markup
from calendarapi.admin.common import AdminModelView
from flask_admin import form
from wtforms import TextAreaField

file_path = os.path.abspath(os.path.dirname(__name__))
hero_dir = os.path.join(file_path, "calendarapi", "static", "team")


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

    def _format_description(view, context, model, name):
        return Markup(model.description)

    def _list_thumbnail():
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            url = url_for("static", filename=os.path.join("/team/", model.photo_path))
            if model.photo_path.split(".")[-1] in ["jpg", "jpeg", "png", "svg", "gif"]:
                return Markup(f"<img src={url} width=320 height=240>")

        return thumbnail_formatter

    column_formatters = {
        "photo_path": _list_thumbnail(),
        "description": _format_description,
    }

    def generate_image_name(model, file_data):
        return f'{uuid.uuid4().hex[:16]}.{file_data.filename.split(".")[-1]}'

    def validate_directory(form, field):
        upload_folder = os.path.join(file_path, "calendarapi", "static", "team")
        os.makedirs(upload_folder, exist_ok=True)

    form_extra_fields = {
        "photo_path": form.ImageUploadField(
            "Виберіть фото партнера",
            base_path=os.path.join(file_path, "calendarapi", "static", "team"),
            url_relative_path="team/",
            namegen=generate_image_name,
            allowed_extensions=["jpg", "png", "jpeg", "gif"],
            max_size=(1280, 960, True),
            thumbnail_size=(320, 240, True),
            validators=[validate_directory],
        ),
        "description": TextAreaField(
            "Опис", render_kw={"class": "form-control", "rows": 3}
        ),
    }
