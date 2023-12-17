from io import BytesIO
from re import search

from wtforms import ValidationError
from werkzeug.datastructures.file_storage import FileStorage

from calendarapi.commons.exeptions import (
    DATA_REQUIRED,
    INVALID_PASSWORD,
    PASSWORD_LEN_ERROR,
)
from calendarapi.config import IMAGE_FORMATS, IMAGE_SIZE


class ImageValidator:
    def __init__(self, required: bool = True) -> None:
        self.required = required

    def __call__(self, form, field):
        "validate image formats and image with IMAGE_FORMATS and IMAGE_SIZE from config"

        if self.required and not field.object_data and not field.data:
            raise ValidationError(DATA_REQUIRED)
        if field.data:
            file_format = field.data.filename.split(".")[-1]
            if file_format not in IMAGE_FORMATS:
                raise ValidationError(
                    f"Формат файлу {file_format} не підтримується. Завантажте фото у наступних форматах: {', '.join(IMAGE_FORMATS)}."
                )
            buffer = field.data.stream.read()
            content_length = round(len(buffer) / 1024 / 1024, 2)
            if content_length > IMAGE_SIZE:
                raise ValidationError(
                    f"Розмір файлу {content_length} мб. перевищує максимально допустимий {IMAGE_SIZE} мб."
                )
            field.data = FileStorage(
                stream=BytesIO(buffer),
                content_length=content_length,
                content_type=field.data.content_type,
                filename=field.data.filename,
                name=field.data.name,
                headers=field.data.headers,
            )


def validate_password(form, field):
    if len(field.data) < 8 or len(field.data) > 64:
        raise ValidationError(reason=PASSWORD_LEN_ERROR)
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!])[A-Za-z\d@#$%^&+=!?]*$"
    if not search(regex, field.data):
        raise ValidationError(reason=INVALID_PASSWORD)
