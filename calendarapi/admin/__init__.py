from calendarapi.admin.common import (
    AdminModelView,
    CustomAdminIndexView,
    configure_login,
)
from calendarapi.admin.specialization import SpecializationModelView
from calendarapi.admin.user import UserModelView
from calendarapi.admin.city import CityModelView
from calendarapi.admin.lawyer import LawyerModelView
from calendarapi.admin.schedule import ScheduleModelView
from calendarapi.admin.appointment import AppointmentModelView
from calendarapi.admin.visitor import VisitorModelView
from calendarapi.admin.our_team import OurTeamModelView
from calendarapi.admin.news import NewsModelView
from calendarapi.admin.contacts import ContactModelView
from calendarapi.admin.reviews import ReviewsModelView
from calendarapi.admin.about_company import AboutCompanyModelView
from calendarapi.admin.possibilities import PossibilitiesModelView
from calendarapi.admin.client import ClientsModelView
from calendarapi.admin.pro_bono import ProBonoModelView
from calendarapi.admin.hero_block import HeroModelView


__all__ = [
    "AdminModelView",
    "CustomAdminIndexView",
    "configure_login",
    "UserModelView",
    "CityModelView",
    "SpecializationModelView",
    "LawyerModelView",
    "ScheduleModelView",
    "AppointmentModelView",
    "VisitorModelView",
    "OurTeamModelView",
    "NewsModelView",
    "ContactModelView",
    "ReviewsModelView",
    "AboutCompanyModelView",
    "PossibilitiesModelView",
    "ClientsModelView",
    "ProBonoModelView",
    "HeroModelView",
]
