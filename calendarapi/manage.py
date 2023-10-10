import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from calendarapi.extensions import db
    from calendarapi.models import User

    click.echo("create user")
    user = User(
        username="admin", email="admin@gmail.com", password="admin", active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
