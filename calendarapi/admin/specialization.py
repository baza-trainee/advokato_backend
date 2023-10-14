from calendarapi.admin.common import AdminModelView


class SpecializationAdminModelView(AdminModelView):
    column_labels = {
        "specialization_name": "Спеціалізація",
    }

    column_list = ["specialization_name"]

    form_excluded_columns = ["lawyers"]
