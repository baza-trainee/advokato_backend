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
)
from calendarapi.services.fake_data import (
    our_team_data,
    specializations,
    cities,
    contacts,
)
from calendarapi.extensions import db

try:
    from tests.factories import LawyersFactory, ScheduleFactory
except ImportError:
    VERCEL = True


@click.command("init")
@with_appcontext
def init():
    if not VERCEL:
        if db.session.query(User).count() == 0:
            """Create a new admin user, fake lawyers, initial city and specializations lists."""
            click.echo("create user")
            user = User(
                username=current_app.config["ADMIN_DEFAULT_LOGIN"],
                email="admin@gmail.com",
                password=current_app.config["ADMIN_DEFAULT_PASSWORD"],
                is_active=True,
                is_superuser=True,
            )

            contact_list = [Contact(**data) for data in contacts]
            city_list = [City(**data) for data in cities]
            spec_list = [Specialization(**data) for data in specializations]
            db.session.add_all([*city_list, *spec_list, *contact_list])
            db.session.flush()

            fake_schedule: List[Schedule] = ScheduleFactory.create_batch(25)
            fake_lawyers: List[Lawyer] = LawyersFactory.create_batch(25)
            for lawyer in fake_lawyers:
                lawyer.cities = list(sample(city_list, randint(1, 2)))
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

            db.session.add_all([*fake_schedule, user])
            db.session.commit()

            click.echo("created user admin")
            click.echo("Added fake cities")
            click.echo("Added fake Lawyers")
            click.echo("Added fake specializations")
        else:
            click.echo("Users is already exist")
    else:
        click.echo("VERCEL MODE ON")
