from wtforms import TextAreaField
from wtforms.validators import DataRequired

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.validators import validate_text
from calendarapi.commons.exeptions import DATA_REQUIRED, REQ_MAX_LEN
from calendarapi.models import HeroBlock


SLOGAN_INFO = "Перше, що бачать користувачі сайту."
LEFT_TEXT_INFO = "Короткий текст зліва під гаслом."
RIGHT_TEXT_INFO = "Короткий текст справа під гаслом."
SLOGAN_LEN = HeroBlock.slogan.type.length
LEFT_TEXT_LEN = HeroBlock.left_text.type.length
RIGHT_TEXT_LEN = HeroBlock.right_text.type.length


class HeroModelView(AdminModelView):
    can_create = False
    can_delete = False

    column_labels = {
        "slogan": "Гасло",
        "left_text": "Текст зліва",
        "right_text": "Текст справа",
    }

    column_descriptions = {
        "slogan": SLOGAN_INFO,
        "left_text": LEFT_TEXT_INFO,
        "right_text": RIGHT_TEXT_INFO,
    }

    form_extra_fields = {
        "slogan": TextAreaField(
            label="Гасло.",
            render_kw={"class": "form-control", "rows": 1},
            validators=[DataRequired(message=DATA_REQUIRED), validate_text],
            description=REQ_MAX_LEN % SLOGAN_LEN,
        ),
        "left_text": TextAreaField(
            label="Опис зліва.",
            render_kw={"class": "form-control", "rows": 3},
            validators=[DataRequired(message=DATA_REQUIRED), validate_text],
            description=REQ_MAX_LEN % LEFT_TEXT_LEN,
        ),
        "right_text": TextAreaField(
            label="Опис справа.",
            render_kw={"class": "form-control", "rows": 3},
            validators=[DataRequired(message=DATA_REQUIRED), validate_text],
            description=REQ_MAX_LEN % RIGHT_TEXT_LEN,
        ),
    }
