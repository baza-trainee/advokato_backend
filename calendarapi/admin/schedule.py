from datetime import datetime, time, timedelta

from flask_admin.form.validators import CustomFieldListInputRequired
from markupsafe import Markup
from sqlalchemy import and_
from wtforms import DateField, ValidationError
from wtforms.validators import DataRequired, Optional

from calendarapi.admin.base_admin import AdminModelView
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
        for day in range((form.data["end_date"] - form.data["date"]).days + 1):
            date = form.data["date"] + timedelta(days=day)
            if date.weekday() not in [5, 6]:
                list_dates.append(date)

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
            description="Якщо бажаєте додати розклад для певного проміжку часу, а не на 1 день (суботи та неділі пропускаються автоматично). Початкова та кінцева дата включно.",
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
            "description": """При створенні нового запису можна обрати декілька спеціалістів та розклад складеться
для кожного з них. При редагуванні можна обрати лише 1.""",
        },
        "time": {
            "validators": [
                CustomFieldListInputRequired(),
                validate_time_format,
            ],
            "description": Markup(
                """Можна додавати декілька значень розділяючи їх пробілом у наступному вигляді:
<br><ul><li><b>HH:MM</b> приклад: 14:45</li><li><b>HH</b> приклад: 18</li><li><b>start_HH-end_HH</b> приклад: 
12-20 (кожну годину включаючи 12:00 та 20:00)</li>"""
            ),
        },
    }

    def get_query(self):
        current_date = datetime.now().date()
        old_shedules = (
            db.session.query(Schedule).where(Schedule.date < current_date).all()
        )
        for shedule in old_shedules:
            db.session.delete(shedule)
        db.session.commit()
        return super().get_query()

    def _apply_sorting(self, query, joins, sort_column, sort_desc):
        joins = {}
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
            query, joins = super()._apply_sorting(query, joins, sort_column, sort_desc)

        return query, joins

    def _apply_search(self, query, count_query, joins, count_joins, search):
        search = search.strip()
        return super()._apply_search(query, count_query, joins, count_joins, search)

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
