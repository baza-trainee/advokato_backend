from typing import List
import click
from flask import current_app
from flask.cli import with_appcontext
from calendarapi.models import (
    Specialization,
    Lawyer,
    User,
    City,
    Schedule,
)
from random import sample, randint
from tests.factories import LawyersFactory, ScheduleFactory
from calendarapi.extensions import db


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user, fake lawyers, initial city and specializations lists."""
    click.echo("create user")
    user = User(
        username=current_app.config["ADMIN_DEFAULT_LOGIN"],
        email="admin@gmail.com",
        password=current_app.config["ADMIN_DEFAULT_PASSWORD"],
        is_active=True,
    )
    city_list = [
        City(city_name="Київ"),
        City(city_name="Одеса"),
        City(city_name="Миколаїв"),
    ]
    spec_list = [
        Specialization(specialization_name="Цивільна"),
        Specialization(specialization_name="Адміністративна"),
        Specialization(specialization_name="Кримінальна"),
        Specialization(specialization_name="Сімейна"),
        Specialization(specialization_name="Військовий"),
        Specialization(specialization_name="Зруйноване майно"),
        Specialization(specialization_name="Порушення прав людини"),
    ]

    fake_schedule: List[Schedule] = ScheduleFactory.create_batch(10)
    fake_lawyers: List[Lawyer] = LawyersFactory.create_batch(10)

    for lawyer, schedule in zip(fake_lawyers, fake_schedule):
        lawyer.specializations = sample(spec_list, randint(1, 7))
        lawyer.cities = list(sample(city_list, randint(1, 3)))
        schedule.lawyer_id = randint(1, 10)
        schedule.time = ["10:00", "11:00", "12:00", "13:00"]
        lawyer.schedules = [schedule]

    db.session.add_all([user, *city_list, *spec_list, *fake_lawyers, *fake_schedule])
    db.session.commit()
    click.echo("created user admin")
    click.echo(f"Added cities: Kyiv, Odesa, Mykolaiv")
    click.echo(f"Added {len(fake_lawyers)} fake Lawyers")
    click.echo(
        "Added specializations: Цивільна, Адміністративна, Кримінальна, Сімейна, Військовий, Зруйноване майно, Порушення прав людини"
    )
