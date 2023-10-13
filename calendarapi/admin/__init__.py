from calendarapi.admin.common import (
    AdminModelView,
    CustomAdminIndexView,
    configure_login,
)
from calendarapi.admin.specialization import SpecializationAdminModelView
from calendarapi.admin.user import UserAdminModelView
from calendarapi.admin.city import CityAdminModelView
from calendarapi.admin.lawyer import LawyerAdminModelView
from calendarapi.admin.schedule import SheduleModelView

__all__ = [
    "AdminModelView",
    "CustomAdminIndexView",
    "configure_login",
    "UserAdminModelView",
    "CityAdminModelView",
    "SpecializationAdminModelView",
    "LawyerAdminModelView",
    "SheduleModelView",
]
