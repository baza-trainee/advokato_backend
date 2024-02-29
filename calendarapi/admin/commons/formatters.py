import os
from typing import Any

from flask import current_app, request
from markupsafe import Markup


class ThumbnailFormatter:
    def __init__(self, width: int = 240) -> None:
        self.width = width

    def __call__(self, view, context, model, name) -> Any:
        field_value = getattr(model, name)
        if not field_value:
            return ""

        if current_app.config["STORAGE"] == "STATIC":
            url = os.path.join(current_app.config.get("BASE_URL"), field_value)
        else:
            url = field_value

        if field_value.split(".")[-1] in current_app.config["IMAGE_FORMATS"]:
            return Markup(f"<img src={url} width={self.width}>")


def format_as_markup(view, context, model, name):
    return Markup(getattr(model, name))
