from typing import List
import click
from random import sample, randint, choice

from flask import current_app
from flask.cli import with_appcontext

from calendarapi.models import (
    Specialization,
    Lawyer,
    User,
    City,
    Schedule,
    OurTeam,
    Contact,
    AboutCompany,
    Possibilities,
    ProBono,
    News,
    Client,
    Reviews,
    HeroBlock,
)
from calendarapi.models.user_permissions import Permission
from calendarapi.services.fake_data import (
    our_team_data,
    specializations,
    cities,
    contacts,
    about_company,
    possibilities,
    probono,
    news,
    clients,
    reviews,
    hero,
)
from calendarapi.extensions import db


try:
    from tests.factories import LawyersFactory, ScheduleFactory
except ImportError:
    VERCEL = True
else:
    VERCEL = False


@click.command("init")
@with_appcontext
def init():
    if not VERCEL:
        if db.session.query(User).count() == 0:
            """Create a new admin user, fake lawyers, initial city and specializations lists."""
            click.echo("create permission")
            permission_all = Permission(view_name=current_app.config["PERMISSION_ALL"])
            db.session.add(permission_all)
            db.session.flush()
            click.echo("create user")
            user = User(
                username=current_app.config["ADMIN_DEFAULT_LOGIN"],
                email="admin@gmail.com",
                password=current_app.config["ADMIN_DEFAULT_PASSWORD"],
                is_active=True,
            )
            db.session.add(user)
            db.session.flush()
            user.permissions = [permission_all]

            contact_list = [Contact(**data) for data in contacts]
            city_list = [City(**data) for data in cities]
            spec_list = [Specialization(**data) for data in specializations]
            possibilities_list = [Possibilities(**data) for data in possibilities]
            probono_list = [ProBono(**data) for data in probono]
            clients_list = [Client(**data) for data in clients]
            reviews_list = [Reviews(**data) for data in reviews]

            db.session.add_all(
                [
                    *city_list,
                    *spec_list,
                    *contact_list,
                    *possibilities_list,
                    *probono_list,
                    *clients_list,
                    *reviews_list,
                    AboutCompany(**about_company),
                    HeroBlock(**hero),
                ]
            )
            db.session.flush()

            fake_schedule: List[Schedule] = ScheduleFactory.create_batch(25)
            fake_lawyers: List[Lawyer] = LawyersFactory.create_batch(25)
            for lawyer in fake_lawyers:
                lawyer.specializations = sample(spec_list, randint(1, 3))

            db.session.add_all(fake_lawyers)
            db.session.flush()

            our_team_members = [OurTeam(**data) for data in our_team_data]
            db.session.add_all(our_team_members)
            db.session.flush()

            for schedule in fake_schedule:
                lawyer = choice(fake_lawyers)
                schedule.lawyers = [lawyer]
                schedule.lawyer_id = lawyer.id
                schedule.time = ["10:00", "11:00", "12:00", "14:00"]

            db.session.add_all(fake_schedule)
            db.session.commit()

            click.echo("created user admin")
            click.echo("Added cities")
            click.echo("Added fake Lawyers")
            click.echo("Added ProBono_data")
            click.echo("Added news")
            click.echo("Added fake clients")
            click.echo("Added fake reviews")
            click.echo("Added hero")

        else:
            click.echo("Users is already exist")

        if db.session.query(News).count() == 0:
            news_list = [News(**data) for data in news]
            db.session.add_all(news_list)
            db.session.commit()
        else:
            click.echo("News is already exist")
    else:
        click.echo("VERCEL MODE ON")
