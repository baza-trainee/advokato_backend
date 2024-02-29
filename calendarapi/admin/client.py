from wtforms import FileField, TextAreaField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.exeptions import REQ_IMAGE, REQ_IMAGE_RESOLUTION, URL_FORMAT
from calendarapi.commons.utils import custom_delete_file, custom_update_file
from calendarapi.models.clients import Client


LINK_LEN = Client.link.type.length
REQ_PHOTO_PATH = REQ_IMAGE_RESOLUTION % (600, 360)


class ClientsModelView(AdminModelView):
    can_set_page_size = True

    column_labels = {
        "photo_path": "Фото",
        "link": "Посилання",
    }

    column_formatters = {
        "photo_path": ThumbnailFormatter(),
    }

    form_extra_fields = {
        "photo_path": FileField(
            label="Виберіть фото для новини",
            validators=[ImageValidator()],
            description=f"{REQ_IMAGE} {REQ_PHOTO_PATH}",
        ),
        "link": TextAreaField(
            label="Посилання",
            description=URL_FORMAT % LINK_LEN,
        ),
    }
    column_default_sort = [
        ("id", False),
    ]

    def on_model_delete(self, model):
        custom_delete_file(model, "photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        return super().on_model_change(form, model, is_created)
