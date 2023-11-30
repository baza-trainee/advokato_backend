from calendarapi.admin.common import (
    AdminModelView,
    CustomAdminIndexView,
    configure_login,
)
from calendarapi.admin.specialization import SpecializationAdminModelView
from calendarapi.admin.user import UserAdminModelView
from calendarapi.admin.city import CityAdminModelView
from calendarapi.admin.lawyer import LawyerAdminModelView
from calendarapi.admin.schedule import ScheduleModelView
from calendarapi.admin.appointment import AppointmentModelView
from calendarapi.admin.visitor import VisitorModelView
from calendarapi.admin.our_team import OurTeamModelView

__all__ = [
    "AdminModelView",
    "CustomAdminIndexView",
    "configure_login",
    "UserAdminModelView",
    "CityAdminModelView",
    "SpecializationAdminModelView",
    "LawyerAdminModelView",
    "ScheduleModelView",
    "AppointmentModelView",
    "VisitorModelView",
    "OurTeamModelView",
]
