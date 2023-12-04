import os
import uuid

from flask import request
from calendarapi.admin.common import AdminModelView
from markupsafe import Markup
from wtforms import TextAreaField
from cloudinary import uploader
from wtforms import FileField


file_path = os.path.abspath(os.path.dirname(__name__))
our_news_dir = os.path.join(file_path, "calendarapi", "static", "media", "news")


class NewsAdminModelView(AdminModelView):
    can_set_page_size = True

    column_labels = {
        "name": "Назва",
        "description": "Опис",
        "created_at": "Дата",
        "photo_path": "Фото",
    }
    column_sortable_list = [
        "created_at",
    ]
    column_searchable_list = [
        "name",
    ]
    column_default_sort = [
        ("id", False),
    ]

    def _format_description(view, context, model, name):
        return Markup(model.description)

    def _list_thumbnail():
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            # url = os.path.join(request.host_url, "static", "media", "news", model.photo_path)
            url = model.photo_path
            if model.photo_path.split(".")[-1] in [
                "jpg",
                "jpeg",
                "png",
                "svg",
                "gif",
                "webp",
            ]:
                return Markup(f"<img src={url} height=240>")

        return thumbnail_formatter

    column_formatters = {
        "description": _format_description,
        "photo_path": _list_thumbnail(),
    }

    # def generate_image_name(model, file_data):
    #     return f'{uuid.uuid4().hex[:16]}.{file_data.filename.split(".")[-1]}'

    # def validate_directory(form, field):
    #     upload_folder = os.path.join(file_path, "calendarapi", "static", "media", "news")
    #     os.makedirs(upload_folder, exist_ok=True)

    form_extra_fields = {
        "description": TextAreaField(
            "Опис", render_kw={"class": "form-control", "rows": 5}
        ),
        "photo_path": FileField("Виберіть фото для новини"),
        # "photo_path": form.ImageUploadField(
        #     "Виберіть фото для новини",
        #     base_path=os.path.join(file_path, "calendarapi", "static", "media", "news"),
        #     url_relative_path=os.path.join('media', 'news', ''),
        #     namegen=generate_image_name,
        #     allowed_extensions=["jpg", "png", "jpeg", "gif", "webp", "svg"],
        #     validators=[validate_directory],
        # ), #TODO переробити ан filefield
    }

    # def on_model_delete(self, model):
    #     file_path = f"{our_news_dir}/{model.photo_path}"
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
