import click
from flask import current_app
from flask.cli import with_appcontext

from calendarapi.models.specialization import Specialization


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from calendarapi.extensions import db
    from calendarapi.models import User, City

    click.echo("create user")
    user = User(
        username=current_app.config["ADMIN_DEFAULT_LOGIN"],
        email="admin@gmail.com",
        password=current_app.config["ADMIN_DEFAULT_PASSWORD"],
        is_active=True,
    )
    cities = [
        City(city_name="Київ"),
        City(city_name="Одеса"),
        City(city_name="Миколаїв"),
    ]
    specializations = [
        Specialization(specialization_name="Цивільна"),
        Specialization(specialization_name="Адміністративна"),
        Specialization(specialization_name="Кримінальна"),
        Specialization(specialization_name="Сімейна"),
        Specialization(specialization_name="Військовий"),
        Specialization(specialization_name="Зруйноване майно"),
        Specialization(specialization_name="Порушення прав людини"),
    ]

    db.session.add_all([user, *cities, *specializations])
    db.session.commit()
    click.echo("created user admin")
    click.echo("Added cities: Kyiv, Odesa, Mykolaiv")
    click.echo(
        "Added specializations: Цивільна, Адміністративна, Кримінальна, Сімейна, Військовий, Зруйноване майно, Порушення прав людини"
    )
