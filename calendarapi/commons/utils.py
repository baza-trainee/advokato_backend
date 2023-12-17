import os
import uuid

from flask import current_app
from cloudinary import uploader


def generate_media_path(dir_name):
    media_path = os.path.join(
        current_app.config["MEDIA_PATH"], dir_name.lower().replace(" ", "_")
    )
    return media_path


def custom_save_file(media_path: str, file):
    if current_app.config["STORAGE"] == "STATIC":
        os.makedirs(media_path, exist_ok=True)
        url_media_path = os.path.join(*media_path.split(os.path.sep)[-3:])
        file_name = f'{uuid.uuid4().hex[:16]}.{file.filename.split(".")[-1]}'
        file_path = os.path.join(media_path, file_name)
        url_file_path = os.path.join(url_media_path, file_name)
        file.save(file_path)
        return url_file_path
    else:
        upload_result = uploader.upload(file)
        return upload_result["url"]


def custom_delete_file(model, field_name: str):
    media_url = getattr(model, field_name, None)
    if media_url:
        media_path = generate_media_path(model.__tablename__)
        if current_app.config["STORAGE"] == "STATIC":
            file_name = media_url.split(os.path.sep)[-1]
            file_path = os.path.join(media_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)


def custom_update_file(model, form, field_name: str):
    media_path = generate_media_path(model.__tablename__)
    field_data = getattr(model, field_name, None)
    db_data = getattr(form, field_name, None).object_data
    if field_data:
        setattr(model, field_name, db_data)  # for delete
        if db_data:
            custom_delete_file(model, field_name=field_name)
        media_url = custom_save_file(media_path, field_data)
        setattr(model, field_name, media_url)
    else:
        setattr(model, field_name, db_data)
