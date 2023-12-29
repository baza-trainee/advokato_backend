from datetime import datetime

from sqlalchemy.orm import joinedload

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.models import Visitor
from calendarapi.extensions import db
from calendarapi.models.appointment import Appointment


SPECIALIZATION_LEN = Appointment.specialization.type.length
LAWYER_LEN = Appointment.lawyer.type.length


class AppointmentModelView(AdminModelView):
    can_set_page_size = True
    can_create = False
    can_edit = True
    can_export = True
    export_types = [
        "csv",
        # "xls",
        # "xlsx",
        # "json",
        # "yaml",
        # "html",
    ]

    column_labels = {
        "visitor_id": "Клієнт",
        "lawyers": "Спеціалісти",
        "visitor": "Клієнт",
        "lawyer": "Адвокат",
        "specialization": "Спеціалізація",
        "appointment_date": "Дата",
        "appointment_time": "Час",
    }

    column_list = [
        "specialization",
        "lawyer",
        "visitor",
        "appointment_date",
    ]

    def _time_formatters(view, context, model, name):
        if model.time:
            return [item.strftime("%H:%M") for item in model.time]
        else:
            return ""

    def _date_formatters(view, context, model, name):
        return datetime.combine(
            model.appointment_date, model.appointment_time
        ).strftime("%d/%m/%Y, %H:%M")

    column_formatters = {
        "visitor": lambda view, context, model, name: db.session.query(Visitor)
        .filter(Visitor.id == model.visitor_id)
        .one_or_none(),
        "time": _time_formatters,
        "appointment_date": _date_formatters,
    }

    column_searchable_list = [
        "specialization",
        "lawyer",
        "appointment_date",
        "visitor_id",
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
            query = query.join(Visitor, Visitor.id == Appointment.visitor_id)
            self._search_fields.extend(
                [
                    [Visitor.email, []],
                    [Visitor.name, []],
                    [Visitor.phone_number, []],
                ]
            )
            query, count_query, joins, count_joins = self._apply_search(
                query, count_query, joins, count_joins, search
            )

        # Apply filters
        if filters and self._filters:
            query, count_query, joins, count_joins = self._apply_filters(
                query, count_query, joins, count_joins, filters
            )

        # Calculate number of rows if necessary
        count = count_query.scalar() if count_query else None

        # Auto join
        for j in self._auto_joins:
            query = query.options(joinedload(j))

        # Sorting
        query, joins = self._apply_sorting(query, joins, sort_column, sort_desc)

        # Pagination
        query = self._apply_pagination(query, page, page_size)

        # Execute if needed
        if execute:
            query = query.all()

        return count, query
