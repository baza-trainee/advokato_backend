import click
from flask import current_app
from flask.cli import with_appcontext


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
        City(city_name="Kyiv"),
        City(city_name="Odesa"),
        City(city_name="Mykolaiv"),
    ]
    db.session.add_all([user, *cities])
    db.session.commit()
    click.echo("created user admin")
    click.echo("Added cities: Kyiv, Odesa, Mykolaiv")
