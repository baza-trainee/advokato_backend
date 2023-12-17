from flask import Flask
from flask_sqlalchemy import record_queries
from flask_admin import Admin
from flask_babel import Babel
from flask_mail import Mail
from markupsafe import Markup
from flask_swagger_ui import get_swaggerui_blueprint

from calendarapi import api, manage
from calendarapi.admin.our_team import OurTeamModelView
from calendarapi.extensions import (
    db,
    migrate,
    # celery,
    # cache,
)
from calendarapi.admin import (
    UserModelView,
    CustomAdminIndexView,
    CityModelView,
    configure_login,
    LawyerModelView,
    ScheduleModelView,
    SpecializationModelView,
    AppointmentModelView,
    VisitorModelView,
    NewsModelView,
    ContactModelView,
    ReviewsModelView,
    AboutCompanyModelView,
    PossibilitiesModelView,
    ClientsModelView,
    ProBonoModelView,
    HeroModelView,
)
from calendarapi.models import (
    User,
    City,
    Lawyer,
    Schedule,
    Specialization,
    Appointment,
    Visitor,
    OurTeam,
    News,
    Contact,
    Reviews,
    AboutCompany,
    Possibilities,
    Client,
    ProBono,
    HeroBlock,
)


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("calendarapi")
    app.config.from_object("calendarapi.config")
    Babel(app)
    if testing is True:
        app.config["TESTING"] = True
        app.config["CACHE_TYPE"] = "null"
    configure_login(app)
    register_adminsite(app)
    configure_extensions(app)
    configure_cli(app)
    configure_mails(app)
    register_blueprints(app)
    # init_celery(app)
    # if app.config["DEBUG"]:
    #     app.after_request(sql_debug)
    return app


def register_adminsite(app):
    base_url = app.config["MAIN_PAGE_URL"]
    header = f'<a href="{base_url}" title="На домашню сторінку Status-AC">\
               <img src="/static/interface/admin_logo.png" height="40px" width="140px" alt="admin_logo" style="margin-right: 30px;"></a>'
    admin = Admin(
        app,
        Markup(header),
        index_view=CustomAdminIndexView(),
        base_template="master.html",
        template_mode="bootstrap4",
    )
    admin.add_view(
        HeroModelView(HeroBlock, db.session, name='"HERO" блок', category="Керування")
    )
    admin.add_view(
        AboutCompanyModelView(
            AboutCompany, db.session, name="Про компанію", category="Керування"
        )
    )
    admin.add_view(
        PossibilitiesModelView(
            Possibilities, db.session, name="Сильні сторони", category="Керування"
        )
    )
    admin.add_view(
        OurTeamModelView(OurTeam, db.session, name="Команда", category="Керування")
    )
    admin.add_view(
        SpecializationModelView(
            Specialization, db.session, name="Cпеціалізації", category="Керування"
        )
    )
    admin.add_view(NewsModelView(News, db.session, name="Новини", category="Керування"))
    admin.add_view(
        ReviewsModelView(Reviews, db.session, name="Відгуки", category="Керування")
    )
    admin.add_view(
        ProBonoModelView(ProBono, db.session, name="ProBono", category="Керування")
    )
    admin.add_view(
        ClientsModelView(Client, db.session, name="Партнери", category="Керування")
    )
    admin.add_view(
        CityModelView(City, db.session, name="Філіали", category="Керування")
    )
    admin.add_view(
        ContactModelView(Contact, db.session, name="Контакти", category="Керування")
    )
    admin.add_view(
        UserModelView(User, db.session, name="Облікові записи", category="Керування")
    )
    admin.add_view(LawyerModelView(Lawyer, db.session, name="Спеціалісти"))
    admin.add_view(ScheduleModelView(Schedule, db.session, name="Розклад"))
    admin.add_view(AppointmentModelView(Appointment, db.session, name="Записи"))
    admin.add_view(VisitorModelView(Visitor, db.session, name="Клієнти"))


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    # cache.init_app(app)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_swagger(app):
    swagger_ui_blueprint = get_swaggerui_blueprint(
        base_url=app.config["SWAGGER_URL"],
        api_url=app.config["SWAGGER_PATH"],
        config=app.config["SWAGGER_CONFIG"],
    )
    return swagger_ui_blueprint


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(
        configure_swagger(app),
        url_prefix=app.config["SWAGGER_URL"],
    )


# def init_celery(app=None):
#     app = app or create_app()
#     celery.conf.update(app.config.get("CELERY", {}))

#     class ContextTask(celery.Task):
#         """Make celery tasks work with Flask app context"""

#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery


def sql_debug(response):
    queries = record_queries.get_recorded_queries()
    total_duration = 0.0
    for query in queries:
        total_duration += query.duration
    print("=" * 80)
    print(
        " SQL Queries - {0} Queries Executed in {1}ms".format(
            len(queries), round(total_duration * 1000, 2)
        )
    )
    return response


def configure_mails(app):
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    Mail(app)
