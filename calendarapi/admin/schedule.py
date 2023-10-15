from datetime import datetime

from wtforms import DateField, ValidationError
from wtforms.validators import DataRequired

from calendarapi.admin.common import AdminModelView
from calendarapi.models.schedule import Schedule


# example for validators with args
class MaxItemsValidator:
    def __init__(self, max_items):
        self.max_items = max_items

    def __call__(self, form, field):
        if field.data and len(field.data) > self.max_items:
            raise ValidationError(f"Можна обрати не більше {self.max_items}")


# example for validators without args
def validate_time_format(form, field):
    try:
        for time in field.data:
            if time.count(":") > 1:
                time_format = "%H:%M:%S"
            else:
                time_format = "%H:%M"
            datetime.strptime(time, time_format)
    except ValueError:
        raise ValidationError("Invalid time format. Use 'HH:MM:SS' or 'HH:MM'.")


def validate_lawyers_for_date(form, field):
    lawyers = form.data.get("lawyers")

    lawyer_id = form.data["lawyers"][0].id if lawyers else None
    date = form.data.get("date")
    schedule_id = (
        form._obj.id if form._obj else None
    )  # _obj - old object from edit form
    existing_schedule = Schedule.query.filter_by(lawyer_id=lawyer_id, date=date).first()

    if existing_schedule and existing_schedule.id != schedule_id:
        raise ValidationError(
            f"У {existing_schedule.lawyers[0]} вже є створена запис на {date}"
        )


class SheduleModelView(AdminModelView):
    column_labels = {
        "lawyers": "Адвокат",
        "time": "Доступний час",
        "date": "Дата",
    }

    column_list = [
        "lawyers",
        "date",
        "time",
    ]

    form_columns = [
        "lawyers",
        "date",
        "time",
    ]

    form_ajax_refs = {
        "lawyers": {
            "fields": ("id",),
            "placeholder": "Оберіть адвоката",
            "minimum_input_length": 0,
        },
    }

    form_extra_fields = {
        "date": DateField(validators=[validate_lawyers_for_date]),
    }

    column_formatters = {
        "time": lambda view, context, model, name: [
            item.strftime("%H:%M") for item in model.time
        ]
        if model.time
        else "",
    }

    column_editable_list = [
        "date",
    ]

    form_args = {
        "lawyers": {
            "label": "Адвокат",
            "validators": [DataRequired(), MaxItemsValidator(max_items=1)],
        },
        "time": {
            "validators": [validate_time_format],
        },
    }

    def on_model_change(self, form, model, is_created):
        if form.data["lawyers"]:
            for lawyer in form.data["lawyers"]:
                model.lawyer_id = lawyer.id  # save to db
