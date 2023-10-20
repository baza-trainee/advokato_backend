from datetime import datetime

from calendarapi.admin.common import AdminModelView
from calendarapi.models import Lawyer, City, Specialization, Visitor
from calendarapi.extensions import db


class AppointmentModelView(AdminModelView):
    can_set_page_size = True
    can_create = False
    can_edit = True
    can_export = True
    export_types = [
        "csv",
        "xls",
        "xlsx",
        "json",
        "yaml",
        "html",
    ]

    column_labels = {
        "lawyers": "Адвокати",
        "visitor_id": "ID Клієнта",
        "visitor": "Клієнт",
        "lawyer_id": "Адвокат",
        "city_id": "Місто",
        "specialization_id": "Спеціалізація",
        "appointment_date": "Дата",
    }

    column_list = [
        "city_id",
        "specialization_id",
        "lawyer_id",
        "visitor",
        "appointment_date",
    ]

    column_formatters = {
        "visitor": lambda view, context, model, name: db.session.query(Visitor)
        .filter(Visitor.id == model.visitor_id)
        .one_or_none(),
        "time": lambda view, context, model, name: [
            item.strftime("%H:%M") for item in model.time
        ]
        if model.time
        else "",
        "lawyer_id": lambda view, context, model, name: db.session.query(Lawyer)
        .filter(Lawyer.id == model.lawyer_id)
        .one_or_none(),
        "city_id": lambda view, context, model, name: db.session.query(City)
        .filter(City.id == model.city_id)
        .one_or_none(),
        "specialization_id": lambda view, context, model, name: db.session.query(
            Specialization
        )
        .filter(Specialization.id == model.specialization_id)
        .one_or_none(),
        "appointment_date": lambda view, context, model, name: datetime.combine(
            model.appointment_date, model.appointment_time
        ).strftime("%d/%m/%Y, %H:%M"),
    }
