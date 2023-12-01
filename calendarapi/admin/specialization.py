from markupsafe import Markup

from wtforms.validators import DataRequired
from calendarapi.admin.common import AdminModelView
from calendarapi.extensions import db
from markupsafe import Markup
from calendarapi.admin.common import AdminModelView
from flask_admin import form
from wtforms import TextAreaField
from cloudinary import uploader
from wtforms import FileField


class SpecializationAdminModelView(AdminModelView):
    form_excluded_columns = ["lawyers"]
    column_list = [
        "specialization_photo",
        "specialization_name",
        "specialization_description",
    ]

    column_labels = {
        "specialization_photo": "Фото",
        "specialization_name": "Спеціалізація",
        "specialization_description": "Опис",
    }

    form_args = {
        "specialization_name": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        },
        "specialization_description": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        },
        "specialization_photo": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        },
    }

    form_columns = [
        "specialization_name",
        "specialization_description",
        "specialization_photo",
    ]

    def _format_description(view, context, model, name):
        return Markup(model.specialization_description)

    def _list_thumbnail():
        def thumbnail_formatter(view, context, model, name):
            if not model.specialization_photo:
                return ""
            # url = os.path.join(request.host_url, "static", "media", "team", model.specialization_photo)
            url = model.specialization_photo
            if model.specialization_photo.split(".")[-1] in [
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
        "specialization_photo": _list_thumbnail(),
        "specialization_description": _format_description,
    }

    # def generate_image_name(model, file_data):
    #     return f'{uuid.uuid4().hex[:16]}.{file_data.filename.split(".")[-1]}'

    # def validate_directory(form, field):
    #     upload_folder = os.path.join(file_path, "calendarapi", "static", "media", "team")
    #     os.makedirs(upload_folder, exist_ok=True)

    form_extra_fields = {
        "specialization_photo": FileField("Виберіть фото для спеціалізації"),
        # "specialization_photo": form.ImageUploadField(
        #     "Виберіть фото партнера",
        #     base_path=os.path.join(file_path, "calendarapi", "static", "media", "team"),
        #     url_relative_path=os.path.join('media', 'team', ''),
        #     namegen=generate_image_name,
        #     allowed_extensions=["jpg", "png", "jpeg", "gif", "webp", "svg"],
        #     validators=[validate_directory],
        # ),
        "specialization_description": TextAreaField(
            "Опис", render_kw={"class": "form-control", "rows": 3}
        ),
    }

    # def on_model_delete(self, model):
    #     file_path = f"{our_team_dir}/{model.specialization_photo}"
    #     if os.path.exists(file_path):
    #         os.remove(file_path)
    #     return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        if model.specialization_photo:
            upload_result = uploader.upload(model.specialization_photo)
            model.specialization_photo = upload_result["url"]
        else:
            model.specialization_photo = form.specialization_photo.object_data
        return super().on_model_change(form, model, is_created)
