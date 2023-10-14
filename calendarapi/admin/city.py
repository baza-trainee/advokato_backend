from calendarapi.admin.common import AdminModelView


class CityAdminModelView(AdminModelView):
    column_labels = {
        "id": "id",
        "city_name": "Місто",
    }

    column_list = ["id", "city_name"]

    form_excluded_columns = ["lawyers"]
