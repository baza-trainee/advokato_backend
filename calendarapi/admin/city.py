from calendarapi.admin.common import AdminModelView


class CityAdminModelView(AdminModelView):
    column_labels = {
        "city_name": "Місто",
    }

    column_list = ["city_name"]

    form_excluded_columns = ["lawyers"]
