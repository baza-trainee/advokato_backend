from markupsafe import Markup

from calendarapi.admin.common import AdminModelView
from calendarapi.models import City, Lawyer
from calendarapi.extensions import db


class CityAdminModelView(AdminModelView):
    form_excluded_columns = ["lawyers"]
    column_labels = {"city_name": "Місто", "lawyers_info": "Інфо"}

    column_list = ["city_name", "lawyers_info"]

    def lawyers_info_formatter(view, context, model, name):
        lawyers = (
            db.session.query(Lawyer)
            .filter(Lawyer.cities.any(City.id == model.id))
            .all()
        )
        total_lawyers = len(lawyers)
        markup = f"<b style='font-size: 18px';>адвокатів у місті: {total_lawyers}</b>"
        markup += "<hr class='hr_stats_header''>" if total_lawyers else ""
        markup += "<hr>".join(
            [
                str(lawyer)
                + f' ({", ".join(str(specialization) for specialization in lawyer.specializations)})'
                for lawyer in lawyers
            ]
        )
        return Markup(f"<div style='text-align: left;'>{markup}</div>")

    column_formatters = {
        "lawyers_info": lawyers_info_formatter,
    }
