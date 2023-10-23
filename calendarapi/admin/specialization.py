from markupsafe import Markup

from wtforms.validators import DataRequired

from calendarapi.admin.common import AdminModelView
from calendarapi.extensions import db
from calendarapi.models import Lawyer, Specialization


class SpecializationAdminModelView(AdminModelView):
    form_excluded_columns = ["lawyers"]
    column_list = [
        "specialization_name",
        "lawyers_info",
    ]
    column_labels = {
        "specialization_name": "Спеціалізація",
        "lawyers_info": "Інфо",
    }

    form_args = {
        "specialization_name": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        }
    }

    def lawyers_info_formatter(view, context, model, name):
        lawyers = (
            db.session.query(Lawyer)
            .filter(Lawyer.specializations.any(Specialization.id == model.id))
            .all()
        )
        total_lawyers = len(lawyers)
        markup = f"<b style='font-size: 18px';>спеціалізується адвокатів: {total_lawyers}</b>"
        markup += "<hr style='background-color: #04202c;'>" if total_lawyers else ""
        markup += "<hr>".join(
            [
                str(lawyer) + f' ({", ".join(str(city) for city in lawyer.cities)})'
                for lawyer in lawyers
            ]
        )
        return Markup(f"<div style='text-align: left;'>{markup}</div>")

    column_formatters = {
        "lawyers_info": lawyers_info_formatter,
    }
