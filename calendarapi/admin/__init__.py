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
from calendarapi.admin.news import NewsAdminModelView
from calendarapi.admin.contacts import ContactModelView
from calendarapi.admin.reviews import ReviewsAdminModelView
from calendarapi.admin.about_company import AboutCompanyModelView
from calendarapi.admin.possibilities import PossibilitiesModelView
from calendarapi.admin.client import ClientsAdminModelView
from calendarapi.admin.pro_bono import ProBonoAdminModelView


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
    "NewsAdminModelView",
    "ContactModelView",
    "ReviewsAdminModelView",
    "AboutCompanyModelView",
    "PossibilitiesModelView",
    "ClientsAdminModelView",
    "ProBonoAdminModelView",
]
