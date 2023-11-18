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
)
from tests.factories import LawyersFactory, ScheduleFactory
from calendarapi.extensions import db


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user, fake lawyers, initial city and specializations lists."""
    click.echo("create user")
    user = db.session.query(User).one_or_none()
    if not user:

        user = User(
            username=current_app.config["ADMIN_DEFAULT_LOGIN"],
            email="admin@gmail.com",
            password=current_app.config["ADMIN_DEFAULT_PASSWORD"],
            is_active=True,
            is_superuser=True,
        )
        city_list = [
            City(city_name="Київ"),
            City(city_name="Одеса"),
            City(city_name="Миколаїв"),
        ]

        db.session.add_all(city_list)
        db.session.flush()

        spec_list = [
            Specialization(specialization_name="Цивільна"),
            Specialization(specialization_name="Адміністративна"),
            Specialization(specialization_name="Кримінальна"),
            Specialization(specialization_name="Сімейна"),
            Specialization(specialization_name="Військовий"),
            Specialization(specialization_name="Зруйноване майно"),
            Specialization(specialization_name="Порушення прав людини"),
        ]

        db.session.add_all(spec_list)
        db.session.flush()

        fake_schedule: List[Schedule] = ScheduleFactory.create_batch(25)
        fake_lawyers: List[Lawyer] = LawyersFactory.create_batch(25)

        for lawyer in fake_lawyers:
            lawyer.cities = list(sample(city_list, randint(1, 2)))
            lawyer.specializations = sample(spec_list, randint(1, 3))

        db.session.add_all(fake_lawyers)
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
        click.echo("user is exist")
