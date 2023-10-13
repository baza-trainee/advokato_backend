from calendarapi.admin.common import AdminModelView


class LawyerAdminModelView(AdminModelView):
    column_labels = {
        "id": "id",
        "name": "Ім'я",
        "surname": "Прізвище",
        "lawyer_mail": "Пошта",
        "specializations": "Спеціалізації",
    }

    column_list = [
        "id",
        "name",
        "surname",
        "lawyer_mail",
        "cities",
        "specializations",
    ]
    form_columns = [
        "name",
        "surname",
        "lawyer_mail",
        "cities",
        "specializations",
    ]

    form_ajax_refs = {
        "specializations": {
            "fields": ("specialization_name",),
            "placeholder": "Оберіть спеціалізацію",
            "minimum_input_length": 0,
        },
        "cities": {
            "fields": ("city_name",),
            "placeholder": "Оберіть місто",
            "minimum_input_length": 0,
        },
    }
