from datetime import datetime
import json

from flask import Response, abort, request, redirect
from flask_admin import expose
from wtforms import DateField, ValidationError
from wtforms.validators import DataRequired

# TODO imports
from sqlalchemy import exists, or_, and_
from flask_admin.contrib.sqla import ajax


from calendarapi.admin.common import AdminModelView
from calendarapi.models import layers_to_cities
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


class ScheduleModelView(AdminModelView):
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
        # city = request.args.get('city')
        return redirect(f"?city={selected_city}")

    def get_query(self):
        selected_city = request.args.get("city")

        if selected_city and selected_city != "all":
            self.query = db.session.query(Schedule).filter(
                Schedule.lawyers.any(Lawyer.cities.any(City.city_name == selected_city))
            )
        else:
            self.query = db.session.query(Schedule)

        if selected_city and selected_city != "all":
            self.selected_city = selected_city
            self.test = db.session.query(Lawyer).filter(
                Lawyer.cities.any(City.city_name == selected_city)
            )
        else:
            self.selected_city = selected_city
            self.test = db.session.query(Lawyer)

        return self.query

    @expose("/ajax/lookup/")
    def ajax_lookup(self):
        # TODO
        # query_test = self.test # model with select city filter
        select_city = self.selected_city  # select city from path args

        name = request.args.get("name")
        query = request.args.get("query")

        offset = request.args.get("offset", type=int)
        limit = request.args.get("limit", 10, type=int)

        loader = self._form_ajax_refs.get(name)
        print("\n" * 15)
        print(self.__dir__())
        print(self.get_filters())

        # ??
        # self._apply_filters(query=)
        # print('model', loader.model)
        # print('get_list', loader.get_list)
        # print('get_query', loader.get_query)
        # print('filter', loader.filters)
        # print(loader.get_query)
        # self._filter_joins = ['JOIN TEST',]
        if not loader:
            abort(404)

        req = db.session.query(Lawyer).filter(
            Lawyer.cities.any(City.city_name == self.selected_city)
        )
        print(req)  # THIS IS WORK FILTERS

        # loader.filters = ['TEST',]

        data = [loader.format(m) for m in loader.get_list(query, offset, limit)]
        return Response(json.dumps(data), mimetype="application/json")

    column_labels = {
        "lawyers": "Адвокат",
        "lawyers.name": "Ім'я",
        "lawyers.surname": "Прізвище",
        "time": "Доступний час",
        "date": "Дата",
    }

    column_list = [
        "lawyer_id",  # TODO develop - delete it
        "lawyers",
        "date",
        "time",
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
            "validators": [
                DataRequired(message="Це поле обов'язкове поле."),
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
