from wtforms import TextAreaField
from wtforms.validators import DataRequired

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.commons.exeptions import DATA_REQUIRED


class HeroModelView(AdminModelView):
    column_labels = {
        "slogan": "Гасло",
        "left_text": "Текст зліва",
        "right_text": "Текст справа",
    }

    column_list = [
        "slogan",
        "left_text",
        "right_text",
    ]

    form_columns = [
        "slogan",
        "left_text",
        "right_text",
    ]
    column_descriptions = {
        "slogan": "Перше, що бачать користувачі сайту.",
        "left_text": "Короткий текст зліва під гаслом, до 200 символів.",
        "right_text": "Короткий текст справа під гаслом, до 200 символів.",
    }

    can_create = False
    can_delete = False

    form_extra_fields = {
        "slogan": TextAreaField(
            label="Гасло.",
            render_kw={"class": "form-control", "rows": 1},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description="Те, що характеризує компанію. До 30 символів.",
        ),
        "left_text": TextAreaField(
            label="Опис зліва.",
            render_kw={"class": "form-control", "rows": 3},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description="До 200 символів.",
        ),
        "right_text": TextAreaField(
            label="Опис справа.",
            render_kw={"class": "form-control", "rows": 3},
            validators=[DataRequired(message=DATA_REQUIRED)],
            description="До 200 символів.",
        ),
    }
