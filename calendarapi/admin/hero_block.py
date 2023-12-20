from wtforms import TextAreaField
from wtforms.validators import DataRequired

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.commons.exeptions import DATA_REQUIRED, REQ_MAX_LEN


class HeroModelView(AdminModelView):
    can_create = False
    can_delete = False

    column_labels = {
        "slogan": "Гасло",
        "left_text": "Текст зліва",
        "right_text": "Текст справа",
    }

    column_descriptions = {
        "slogan": "Перше, що бачать користувачі сайту.",
        "left_text": "Короткий текст зліва під гаслом.",
        "right_text": "Короткий текст справа під гаслом.",
    }

    form_extra_fields = {
        "slogan": TextAreaField(
            label="Гасло.",
            render_kw={"class": "form-control", "rows": 1},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=REQ_MAX_LEN % 30,
        ),
        "left_text": TextAreaField(
            label="Опис зліва.",
            render_kw={"class": "form-control", "rows": 3},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=REQ_MAX_LEN % 200,
        ),
        "right_text": TextAreaField(
            label="Опис справа.",
            render_kw={"class": "form-control", "rows": 3},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description=REQ_MAX_LEN % 200,
        ),
    }
