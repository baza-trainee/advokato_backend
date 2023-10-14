from wtforms.fields import StringField
from wtforms.validators import DataRequired

from calendarapi.admin.common import AdminModelView


class SpecializationAdminModelView(AdminModelView):
    column_labels = {
        "id": "id",
        "specialization_name": "Спеціалізація",
    }

    column_list = ["id", "specialization_name"]

    form_excluded_columns = ["lawyers"]
