from datetime import datetime
import json

from flask import Response, abort, request, redirect, url_for
from flask_admin import expose
from flask_admin.form.validators import CustomFieldListInputRequired
from sqlalchemy import and_, func, or_
from wtforms import DateField, ValidationError
from wtforms.validators import DataRequired
from sqlalchemy.orm import joinedload

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
    existing_schedule = Schedule.query.filter_by(
        lawyer_id=lawyer_id, date=date
    ).one_or_none()

    if existing_schedule and existing_schedule.id != schedule_id:
        raise ValidationError(
            f"У {existing_schedule.lawyers[0]} вже є створена запис на {date}"
        )


def validate_date_not_lower_than_current(form, field):
    current_date = datetime.now().date()
    if not field.data or field.data < current_date:
        raise ValidationError("Оберіть вірну дату.")


class ScheduleModelView(AdminModelView):
    can_set_page_size = True
    list_template = "admin/custom_list.html"
    current_city = "Оберіть місто"

    def _reset_current_city(self):
        self.current_city = "Оберіть місто"

    def get_cities(self):
        cities = db.session.query(City).all()
        return cities

    @expose("/", methods=["POST"])
    def get_selected_city(self):
        selected_city = request.form.get("city")

        if selected_city == "Усі міста" or not selected_city:
            self._reset_current_city()
            selected_city = None

        self.current_city = selected_city
        return redirect(
            f"?city={selected_city}"
            if selected_city
            else url_for("schedule.get_selected_city")
        )

    def get_query(self):
        self.selected_city = request.args.get("city")
        if self.selected_city:
            self.query = db.session.query(Schedule).filter(
                Schedule.lawyers.any(
                    Lawyer.cities.any(City.city_name == self.selected_city)
                )
            )
        else:
            self._reset_current_city()
            self.query = db.session.query(Schedule)
        return self.query

    @expose("/ajax/lookup/")
    def ajax_lookup(self):
        # selected_city = self.selected_city  # select city from path args
        name = request.args.get("name")
        query = request.args.get("query")
        offset = request.args.get("offset", type=int)
        limit = request.args.get("limit", 10, type=int)
        loader = self._form_ajax_refs.get(name)
        if not loader:
            abort(404)

        # if selected_city is None or selected_city == "all":
        if True:
            data = [loader.format(m) for m in loader.get_list(query, offset, limit)]
        # else:
        #     sql_query = (
        #         db.session.query(Lawyer)
        #         .filter(
        #             and_(
        #                 Lawyer.cities.any(City.city_name == selected_city),
        #                 or_(
        #                     Lawyer.name.ilike(f"%{query}%"),
        #                     Lawyer.surname.ilike(f"%{query}%"),
        #                 ),
        #             )
        #         )
        #         .offset(offset)
        #         .limit(limit)
        #     )
        #     lawyer_list_output = [
        #         lawyer
        #         for lawyer in sql_query
        #         if selected_city in [str(city) for city in lawyer.cities]
        #     ]
        #     data = [loader.format(lawyer) for lawyer in lawyer_list_output]

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

    def get_list(
        self,
        page,
        sort_column,
        sort_desc,
        search,
        filters,
        execute=True,
        page_size=None,
    ):
        return super().get_list(
            page, sort_column, sort_desc, search, filters, execute, page_size
        )

    def get_list(
        self,
        page,
        sort_column,
        sort_desc,
        search,
        filters,
        execute=True,
        page_size=None,
    ):
        selected_city = request.args.get("city")

        # Will contain join paths with optional aliased object
        joins = {}
        count_joins = {}

        query = self.get_query()
        count_query = self.get_count_query() if not self.simple_list_pager else None

        # Ignore eager-loaded relations (prevent unnecessary joins)
        # TODO: Separate join detection for query and count query?
        if hasattr(query, "_join_entities"):
            for entity in query._join_entities:
                for table in entity.tables:
                    joins[table] = None

        # Apply search criteria
        if self._search_supported and search:
            query, count_query, joins, count_joins = self._apply_search(
                query, count_query, joins, count_joins, search
            )

        # Apply filters
        if selected_city and selected_city != "all":
            count_query = (
                self.session.query(func.count("*"))
                .select_from(self.model)
                .filter(
                    Schedule.lawyers.any(
                        Lawyer.cities.any(City.city_name == self.selected_city)
                    )
                )
            )
            query = query.filter(
                Schedule.lawyers.any(
                    Lawyer.cities.any(City.city_name == self.selected_city)
                )
            )

        # Calculate number of rows if necessary
        count = count_query.scalar() if count_query else None

        # Auto join
        for j in self._auto_joins:
            query = query.options(joinedload(j))

        # Sorting
        if sort_column == "date":
            if sort_desc:
                query = query.order_by(self.model.date.desc())
            else:
                query = query.order_by(self.model.date)
        elif sort_column == "lawyers":
            if sort_desc:
                query = query.order_by(self.model.lawyer_id.desc())
            else:
                query = query.order_by(self.model.lawyer_id)
        else:
            query, joins = self._apply_sorting(query, joins, sort_column, sort_desc)

        # Pagination
        query = self._apply_pagination(query, page, page_size)

        # Execute if needed
        if execute:
            query = query.all()

        return count, query

    column_sortable_list = [
        "id",
        "lawyers",
        "date",
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
        "date": DateField(
            label="Дата",
            validators=[
                validate_lawyers_for_date,
                validate_date_not_lower_than_current,
            ],
            default=datetime.now().date(),
        ),
    }

    column_formatters = {
        "time": lambda view, context, model, name: [
            item.strftime("%H:%M") for item in model.time
        ]
        if model.time
        else "",
    }

    form_args = {
        "lawyers": {
            "label": "Адвокат",
            "validators": [
                DataRequired(message="Це поле обов'язкове."),
                MaxItemsValidator(max_items=1),
            ],
        },
        "time": {
            "validators": [
                CustomFieldListInputRequired(),
                validate_time_format,
            ],
        },
    }

    def on_model_change(self, form, model, is_created):
        if form.data["lawyers"]:
            for lawyer in form.data["lawyers"]:
                model.lawyer_id = lawyer.id  # save to db
        if form.data["time"]:
            res = list(set(_validate_time_format(form.data["time"])))
            res.sort()
            model.time = res
