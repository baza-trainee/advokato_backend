from datetime import datetime
import json

from flask import Response, abort, request, redirect
from flask_admin import expose
from sqlalchemy import and_, or_
from wtforms import DateField, ValidationError
from wtforms.validators import DataRequired

from calendarapi.admin.common import AdminModelView
from calendarapi.models.city import City
from calendarapi.models.lawyer import Lawyer
from calendarapi.models.schedule import Schedule
from calendarapi.extensions import db


# example for validators with args
class MaxItemsValidator:
    def __init__(self, max_items):
        self.max_items = max_items

    def __call__(self, form, field):
        if field.data and len(field.data) > self.max_items:
            raise ValidationError(f"Можна обрати не більше {self.max_items}.")


# example for validators without args
def validate_time_format(form, field):
    _validate_time_format(field.data)


def _validate_time_format(time_list):
    try:
        res = list()
        for time in time_list:
            if time.count(":") > 1:
                time_format = "%H:%M:%S"
            elif time.count(":") == 1:
                time_format = "%H:%M"
            else:
                time_format = "%H"
            res.append(datetime.strptime(time, time_format).time())
        return res

    except ValueError:
        raise ValidationError(
            "Невірний формат. Приймається час у вигляді 'HH:MM:SS' або 'HH:MM' або 'HH'."
        )


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


class ScheduleModelView(AdminModelView):
    can_set_page_size = True
    list_template = "admin/custom_list.html"
    current_city = "Оберіть місто"

    def get_item(self):
        cities = db.session.query(City).all()
        return cities

    @expose("/", methods=["GET", "POST"])
    def test_view(self):
        selected_city = request.form.get("city")
        if selected_city == "Усі міста":
            self.current_city = "Оберіть місто"
            selected_city = "all"
        else:
            self.current_city = selected_city
        return redirect(f"?city={selected_city}")

    def get_query(self):
        self.selected_city = request.args.get("city")
        if self.selected_city and self.selected_city != "all":
            self.query = db.session.query(Schedule).filter(
                Schedule.lawyers.any(
                    Lawyer.cities.any(City.city_name == self.selected_city)
                )
            )
        else:
            self.query = db.session.query(Schedule)
        return self.query

    @expose("/ajax/lookup/")
    def ajax_lookup(self):
        select_city = self.selected_city  # select city from path args
        name = request.args.get("name")
        query = request.args.get("query")
        offset = request.args.get("offset", type=int)
        limit = request.args.get("limit", 10, type=int)
        loader = self._form_ajax_refs.get(name)
        if not loader:
            abort(404)

        if select_city is None or select_city == "all":
            data = [loader.format(m) for m in loader.get_list(query, offset, limit)]
        else:
            sql_query = (
                db.session.query(Lawyer)
                .filter(
                    and_(
                        Lawyer.cities.any(City.city_name == select_city),
                        or_(
                            Lawyer.name.ilike(f"%{query}%"),
                            Lawyer.surname.ilike(f"%{query}%"),
                        ),
                    )
                )
                .offset(offset)
                .limit(limit)
            )
            lawyer_list_output = [
                lawyer
                for lawyer in sql_query
                if select_city in [str(city) for city in lawyer.cities]
            ]
            data = [loader.format(lawyer) for lawyer in lawyer_list_output]

        return Response(json.dumps(data), mimetype="application/json")

    column_labels = {
        "lawyers": "Адвокат",
        "lawyers.name": "Ім'я",
        "lawyers.surname": "Прізвище",
        "time": "Доступний час",
        "date": "Дата",
    }

    column_list = [
        "lawyers",
        "date",
        "time",
    ]

    column_sortable_list = [
        "lawyers.name",
    ]

    column_searchable_list = [
        "lawyers.name",
        "lawyers.surname",
    ]

    form_columns = [
        "lawyers",
        "date",
        "time",
    ]

    form_ajax_refs = {
        "lawyers": {
            "fields": ("name",),
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
            "validators": [
                DataRequired(message="Це поле обов'язкове."),
                MaxItemsValidator(max_items=1),
            ],
        },
        "time": {
            "validators": [validate_time_format],
        },
    }

    def on_model_change(self, form, model, is_created):
        if form.data["lawyers"]:
            for lawyer in form.data["lawyers"]:
                model.lawyer_id = lawyer.id  # save to db
        if form.data["time"]:
            res = _validate_time_format(form.data["time"])
            model.time = res
