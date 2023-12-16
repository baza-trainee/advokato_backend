from datetime import datetime, time, timedelta

from flask import request
from flask_admin.form.validators import CustomFieldListInputRequired
from markupsafe import Markup
from sqlalchemy import and_
from wtforms import DateField, ValidationError
from wtforms.validators import DataRequired, Optional
from sqlalchemy.orm import joinedload

from calendarapi.admin.common import AdminModelView
from calendarapi.models.schedule import Schedule
from calendarapi.extensions import db


def validate_lawyers(form, field):
    if not form.data["end_date"] and len(form.data["lawyers"]) > 1:
        raise ValidationError("При редагуванні можна обрати лише одного спеціаліста.")


def validate_end_date(form, field):
    if form.data["end_date"] and form.data["end_date"] < form.data["date"]:
        raise ValidationError("Кінцева дата не може бути раніше початкової.")


def validate_date(form, field):
    list_times = _validate_time_format(form.data["time"], skip_raise=True)
    current_date = datetime.now().date()
    if form.data["date"] < current_date:
        raise ValidationError("Дата не повинна бути в минулому.")

    list_dates = [form.data["date"]]
    if form.data["end_date"]:
        list_dates += [
            form.data["date"] + timedelta(days=day)
            for day in range((form.data["end_date"] - form.data["date"]).days + 1)
        ]

    lawyers_shedule = []
    shedule_error = []
    if list_times:
        form._fields["time"].data = [time.strftime("%H:%M") for time in list_times]
        for lawyer in form.data["lawyers"]:
            existing_schedule = (
                db.session.query(Schedule)
                .where(
                    and_(Schedule.lawyer_id == lawyer.id, Schedule.date.in_(list_dates))
                )
                .all()
            )
            existing_schedule = set(lawyer.date for lawyer in existing_schedule)
            success_shedule = set(list_dates) - existing_schedule
            if not success_shedule and (
                form._obj and form._obj.date in existing_schedule
            ):
                success_shedule = [form._obj.date]
                existing_schedule -= {form._obj.date}
            for date in success_shedule:
                shedule = Schedule(
                    lawyer_id=lawyer.id, time=list_times, date=date, lawyers=[lawyer]
                )
                lawyers_shedule.append(shedule)
            if existing_schedule:
                shedule_error.append(
                    {
                        "lawyer": lawyer,
                        "existing_schedule": existing_schedule,
                    }
                )
        if shedule_error:
            err = ""
            for shedule in shedule_error:
                if shedule != shedule_error[0]:
                    err += "<li>"
                err += (
                    f"У спеціаліста <b>{shedule['lawyer']}</b> вже були записи на:<br>"
                )
                for date in shedule["existing_schedule"]:
                    err += f"- {date}<br>"
                if shedule != shedule_error[0]:
                    err += "</li>"
            err += f"<br>Оберіть іншу дату або видаліть існуючу у розкладі"
            raise ValidationError(Markup(err))

        if lawyers_shedule:
            form_model = lawyers_shedule.pop()
            form.date.data = form_model.date
            form.lawyers.data = form_model.lawyers
            form.lawyers.data = form_model.lawyers
            form.time.data = form_model.time
            db.session.add_all(lawyers_shedule)


def validate_time_format(form, field):
    res = _validate_time_format(field.data)
    return res


def _validate_time_format(time_list: list, skip_raise=False) -> list[time]:
    try:
        if time_list and isinstance(time_list[0], str):
            res = list()
            for time in time_list:
                if time.count("-") == 1:
                    start_time, end_time = map(int, time.split("-"))
                    if end_time < start_time:
                        raise SyntaxError(f"{start_time}-{end_time}")
                    time_list.extend(map(str, range(start_time, end_time + 1)))
                    continue
                if time.count(":") > 1:
                    time_format = "%H:%M:%S"
                elif time.count(":") == 1:
                    time_format = "%H:%M"
                else:
                    time_format = "%H"
                res.append(datetime.strptime(time, time_format).time())
            res = list(set(res))
            res.sort()
            return res
    except SyntaxError as exc:
        if not skip_raise:
            raise ValidationError(f"{exc.msg} <start_HH> не може бути менше <end_HH>")
    except ValueError:
        if not skip_raise:
            raise ValidationError(
                "Невірний формат. Приймається час у вигляді'HH:MM' або 'HH' або start_HH-end_HH. HH(0-23) MM(0-59)."
            )


class ScheduleModelView(AdminModelView):
    can_set_page_size = True
    # list_template = "admin/custom_list.html"
    # current_lawyer = "Оберіть юриста"

    # def _reset_current_lawyer(self):
    #     self.current_lawyer = "Оберіть юриста"

    # def get_lawyers(self):
    #     lawyers = db.session.query(Lawyer).all()
    #     return lawyers

    # @expose("/", methods=["POST"])
    # def get_selected_lawyer(self):
    #     selected_lawyer = request.form.get("lawyer")

    #     if selected_lawyer == "Усі юристи" or not selected_lawyer:
    #         self._reset_current_lawyer()
    #         selected_lawyer = None

    #     self.current_lawyer = selected_lawyer
    #     return redirect(f"?lawyer={selected_lawyer}" if selected_lawyer else url_for("schedule.get_selected_lawyer"))

    # def get_query(self):
    #     self.selected_lawyer = request.args.get("lawyer")
    #     if self.selected_lawyer:
    #         self.query = db.session.query(Schedule).filter(Schedule.lawyers.any(Lawyer.name == self.selected_lawyer))
    #     else:
    #         self._reset_current_lawyer()
    #         self.query = db.session.query(Schedule)
    #     return self.query

    def get_query(self):
        current_date = datetime.now().date()
        old_shedules = (
            db.session.query(Schedule).where(Schedule.date < current_date).all()
        )
        for shedule in old_shedules:
            db.session.delete(shedule)
        db.session.commit()
        return super().get_query()

    # @expose("/ajax/lookup/")
    # def ajax_lookup(self):
    #     selected_city = self.selected_city  # select city from path args
    #     name = request.args.get("name")
    #     query = request.args.get("query")
    #     offset = request.args.get("offset", type=int)
    #     limit = request.args.get("limit", 10, type=int)
    #     loader = self._form_ajax_refs.get(name)
    #     if not loader:
    #         abort(404)

    #     if selected_city is None or selected_city == "all":
    #         data = [loader.format(m) for m in loader.get_list(query, offset, limit)]
    #     else:
    #         sql_query = (
    #             db.session.query(Lawyer)
    #             .filter(
    #                 and_(
    #                     Lawyer.cities.any(City.city_name == selected_city),
    #                     or_(
    #                         Lawyer.name.ilike(f"%{query}%"),
    #                     ),
    #                 )
    #             )
    #             .offset(offset)
    #             .limit(limit)
    #         )
    #         lawyer_list_output = [
    #             lawyer
    #             for lawyer in sql_query
    #             if selected_city in [str(city) for city in lawyer.cities]
    #         ]
    #         data = [loader.format(lawyer) for lawyer in lawyer_list_output]

    #     return Response(json.dumps(data), mimetype="application/json")

    column_labels = {
        "lawyers": "Спеціалісти",
        "lawyers.name": "Спеціаліст",
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
        selected_lawyer = request.args.get("lawyer")

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
            search = search.strip()
            query, count_query, joins, count_joins = self._apply_search(
                query, count_query, joins, count_joins, search
            )

        # Apply filters
        # if selected_lawyer and selected_lawyer != "all": #TODO (для відображення кількості в СПИСОК)
        #     count_query = (
        #         self.session.query(func.count("*"))
        #         .select_from(self.model)
        #         .filter(Schedule.lawyers.any(Lawyer.cities.any(City.city_name == self.selected_lawyer)))
        #     )
        #     query = query.filter(Schedule.lawyers.any(Lawyer.name == self.selected_lawyer))

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
        "date",
    ]

    form_columns = [
        "lawyers",
        "date",
        "end_date",
        "time",
    ]

    form_ajax_refs = {
        "lawyers": {
            "fields": ("name",),
            "placeholder": "Оберіть спеціаліста",
            "minimum_input_length": 0,
        },
    }
    form_extra_fields = {
        "date": DateField(
            label="Дата",
            validators=[
                DataRequired(),
                validate_date,
            ],
            default=datetime.now().date(),
        ),
        "end_date": DateField(
            label="Кінцева дата",
            validators=[Optional(), validate_end_date],
            description="Якщо бажаєте додати розклад для певного проміжку часу, а не на 1 день. Початкова та кінцева дата включно.",
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
            "label": "Спеціалісти",
            "validators": [
                DataRequired(message="Це поле обов'язкове."),
                validate_lawyers,
            ],
            "description": "При створенні нового запису можна обрати декілька спеціалістів та розклад складеться для кожного з них. При редагуванні можна обирати лише 1.",
        },
        "time": {
            "validators": [
                CustomFieldListInputRequired(),
                validate_time_format,
            ],
            "description": Markup(
                "Можна додавати кілька значень розділяючи їх пробілом у наступному вигляді:<br>"
                + "<ul><li><b>HH:MM</b> приклад: 14:45</li><li><b>HH</b> приклад: 18</li>"
                + "<li><b>start_HH-end_HH</b> приклад: 12-20 (кожну годину включаючи 12:00 та 20:00)</li>"
            ),
        },
    }
    # column_filters = [
    #     "date",
    # ]

    def on_model_change(self, form, model, is_created):
        model.lawyer_id = model.lawyers[0].id
        return super().on_model_change(form, model, is_created)

    def on_form_prefill(self, form, id):
        if form._fields["time"].data and isinstance(form._fields["time"].data[0], time):
            form._fields["time"].data = (
                [time.strftime("%H:%M") for time in form.time.data]
                if form.time.data
                else []
            )
        del form._fields["end_date"]
        return super().on_form_prefill(form, id)
