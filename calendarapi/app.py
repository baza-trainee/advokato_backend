from flask import Flask
from flask_sqlalchemy import record_queries
from flask_admin import Admin
from flask_babel import Babel
from flask_mail import Mail
from markupsafe import Markup

from calendarapi import api, manage
from calendarapi.admin.our_team import OurTeamModelView
from calendarapi.extensions import (
    apispec,
    db,
    migrate,
    celery,
    cache,
)
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
    NewsAdminModelView,
    ContactModelView,
    ReviewsAdminModelView,
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
)
from calendarapi.api.schemas import (
    VisitorSchema,
    CitySchema,
    LawyerSchema,
    SpecializationSchema,
    AppointmentSchema,
    ScheduleSchema,
    OurTeamSchema,
    NewsSchema,
    ReviewsSchema,
)
from calendarapi.api.resources import (
    CityListResource,
    SpecializationListByCityResource,
    AllSpecializationsResource,
    LawyersListResource,
    ScheduleResource,
    AppointmentResource,
    OurTeamResource,
    FeedbackResource,
    NewsResource,
    ContactResource,
    ReviewsResource,
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
    configure_apispec(app)
    configure_mails(app)
    register_blueprints(app)
    init_celery(app)

    with app.app_context():
        apispec.spec.components.schema("VisitorSchema", schema=VisitorSchema)
        apispec.spec.components.schema("CitySchema", schema=CitySchema)
        apispec.spec.components.schema("LawyerSchema", schema=LawyerSchema)
        apispec.spec.components.schema("ScheduleSchema", schema=ScheduleSchema)
        apispec.spec.components.schema(
            "SpecializationSchema", schema=SpecializationSchema
        )
        apispec.spec.components.schema("AppointmentSchema", schema=AppointmentSchema)
        apispec.spec.components.schema("OurTeamSchema", schema=OurTeamSchema)
        apispec.spec.components.schema("NewsSchema", schema=NewsSchema)
        apispec.spec.components.schema("ReviewsSchema", schema=ReviewsSchema)

        apispec.spec.path(view=ScheduleResource, app=app)
        apispec.spec.path(view=AppointmentResource, app=app)
        apispec.spec.path(view=CityListResource, app=app)
        apispec.spec.path(view=LawyersListResource, app=app)
        apispec.spec.path(view=SpecializationListByCityResource, app=app)
        apispec.spec.path(view=AllSpecializationsResource, app=app)
        apispec.spec.path(view=OurTeamResource, app=app)
        apispec.spec.path(view=FeedbackResource, app=app)
        apispec.spec.path(view=NewsResource, app=app)
        apispec.spec.path(view=ContactResource, app=app)
        apispec.spec.path(view=ReviewsResource, app=app)
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
        CityAdminModelView(City, db.session, name="Міста", category="Керування")
    )
    admin.add_view(
        SpecializationAdminModelView(
            Specialization, db.session, name="Cпеціалізації", category="Керування"
        )
    )
    admin.add_view(LawyerAdminModelView(Lawyer, db.session, name="Адвокати"))
    admin.add_view(ScheduleModelView(Schedule, db.session, name="Розклад"))
    admin.add_view(AppointmentModelView(Appointment, db.session, name="Записи"))
    admin.add_view(VisitorModelView(Visitor, db.session, name="Клієнти"))
    admin.add_view(
        OurTeamModelView(OurTeam, db.session, name="Команда", category="Керування")
    )
    admin.add_view(
        NewsAdminModelView(News, db.session, name="Новини", category="Керування")
    )
    admin.add_view(
        ReviewsAdminModelView(Reviews, db.session, name="Відгуки", category="Керування")
    )
    admin.add_view(
        ContactModelView(Contact, db.session, name="Контакти", category="Керування")
    )
    admin.add_view(
        UserAdminModelView(
            User, db.session, name="облікові записи", category="Керування"
        )
    )


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
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
    app.register_blueprint(api.views.blueprint)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


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
