from flask import Flask
from flask_sqlalchemy import record_queries
from flask_admin import Admin
from flask_babel import Babel
from flask_mail import Mail
from markupsafe import Markup

from flask_cors import CORS
from calendarapi import api, auth, manage
from calendarapi.extensions import (
    apispec,
    db,
    migrate,
    # jwt,
    # celery,
)
# from calendarapi.auth.views import (
#     login,
#     refresh,
#     revoke_access_token,
#     revoke_refresh_token,
# )
from calendarapi.admin import (
    UserAdminModelView,
    CustomAdminIndexView,
    CityAdminModelView,
    configure_login,
    LawyerAdminModelView,
    ScheduleModelView,
    SpecializationAdminModelView,
    AppointmentModelView,
    VisitorModelView,
)
from calendarapi.models import (
    User,
    City,
    Lawyer,
    Schedule,
    Specialization,
    Appointment,
    Visitor,
)
from calendarapi.api.schemas import (
    VisitorSchema,
    CitySchema,
    LawyerSchema,
    SpecializationSchema,
    AppointmentSchema,
    ScheduleSchema,
)
from calendarapi.api.resources import (
    CityListResource,
    SpecializationListResource,
    LawyersListResource,
    ScheduleResource,
    AppointmentResource,
)


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("calendarapi")
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object("calendarapi.config")
    Babel(app)
    if testing is True:
        app.config["TESTING"] = True
        app.config["CACHE_TYPE"] = "null"
    configure_login(app)
    register_adminsite(app)
    configure_extensions(app)
    configure_cli(app)
    configure_apispec(app)
    configure_mails(app)
    register_blueprints(app)
    # init_celery(app)
    # if app.config["DEBUG"]:
    #     app.after_request(sql_debug)

    with app.app_context():
        apispec.spec.components.schema("VisitorSchema", schema=VisitorSchema)
        apispec.spec.components.schema("CitySchema", schema=CitySchema)
        apispec.spec.components.schema("LawyerSchema", schema=LawyerSchema)
        apispec.spec.components.schema("ScheduleSchema", schema=ScheduleSchema)
        apispec.spec.components.schema("SpecializationSchema", schema=SpecializationSchema)
        apispec.spec.components.schema("AppointmentSchema", schema=AppointmentSchema)
        apispec.spec.path(view=ScheduleResource, app=app)
        apispec.spec.path(view=AppointmentResource, app=app)
        apispec.spec.path(view=CityListResource, app=app)
        apispec.spec.path(view=LawyersListResource, app=app)
        apispec.spec.path(view=SpecializationListResource, app=app)
        # apispec.spec.path(view=login, app=app)
        # apispec.spec.path(view=refresh, app=app)
        # apispec.spec.path(view=revoke_access_token, app=app)
        # apispec.spec.path(view=revoke_refresh_token, app=app)
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
    admin.add_view(UserAdminModelView(User, db.session, name="Користувачі", category="Керування"))
    admin.add_view(CityAdminModelView(City, db.session, name="Місто"))
    admin.add_view(SpecializationAdminModelView(Specialization, db.session, name="Cпеціалізація"))
    admin.add_view(LawyerAdminModelView(Lawyer, db.session, name="Адвокати"))
    admin.add_view(ScheduleModelView(Schedule, db.session, name="Розклад"))
    admin.add_view(AppointmentModelView(Appointment, db.session, name="Записи"))
    admin.add_view(VisitorModelView(Visitor, db.session, name="Клієнти"))


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    # jwt.init_app(app)
    migrate.init_app(app, db)
    # cache.init_app(app)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme("jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """Register all blueprints for application"""
    # app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)


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
    print(" SQL Queries - {0} Queries Executed in {1}ms".format(len(queries), round(total_duration * 1000, 2)))
    return response


def configure_mails(app):
    app.config["MAIL_SERVER"] = "outlook.office365.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    Mail(app)
