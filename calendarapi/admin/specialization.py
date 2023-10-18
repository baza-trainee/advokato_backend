from wtforms.validators import DataRequired

from calendarapi.admin.common import AdminModelView


class SpecializationAdminModelView(AdminModelView):
    column_list = ["specialization_name"]
    column_labels = {"specialization_name": "Спеціалізація"}

    form_excluded_columns = ["lawyers"]

    form_args = {
        "specialization_name": {
            "validators": [DataRequired(message="Це поле обов'язкове.")],
        }
    }
