import json
from typing import Dict
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
from dotenv import load_dotenv
from calendarapi.models import User, City, Lawyer, Specialization
from calendarapi.app import create_app
from calendarapi.extensions import db as _db
from pytest_factoryboy import register
from click.testing import CliRunner
from tests.factories import (
    UserFactory,
    CityFactory,
    LawyersFactory,
    SpecializationFactory,
    VisitorFactory,
    ScheduleFactory,
)
from calendarapi.app import init_celery
from flask.testing import FlaskClient

register(UserFactory)
register(CityFactory)
register(LawyersFactory)
register(SpecializationFactory)
register(VisitorFactory)
register(ScheduleFactory)


@pytest.fixture(scope="session")
def app() -> Flask:
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture(scope="function")
def db(app: Flask) -> SQLAlchemy:
    _db.app = app

    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def admin_user(db: SQLAlchemy) -> User:
    user = User(username="admin", email="admin@admin.com", password="admin")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture(scope="function")
def runner(app):
    return CliRunner()


@pytest.fixture
def admin_headers(admin_user: User, client: FlaskClient) -> Dict[str, str]:
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["access_token"],
    }


@pytest.fixture
def admin_refresh_headers(admin_user: User, client: FlaskClient) -> Dict[str, str]:
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["refresh_token"],
    }


@pytest.fixture(scope="session")
def celery_session_app(celery_session_app: Celery, app: Flask) -> Celery:
    celery = init_celery(app)

    celery_session_app.conf = celery.conf
    celery_session_app.Task = celery_session_app.Task

    yield celery_session_app


@pytest.fixture(scope="session")
def celery_worker_pool() -> str:
    return "solo"


@pytest.fixture
def city(db: SQLAlchemy) -> City:
    city = City(city_name="Lviv")
    db.session.add(city)
    db.session.commit()
    return city


@pytest.fixture
def lawyer(db: SQLAlchemy, city) -> Lawyer:
    specializations = [
        Specialization(specialization_name="Цивільна"),
        Specialization(specialization_name="Адміністративна"),
    ]
    lawyer = Lawyer(
        cities=1,
        lawyer_mail="emily@example.com",
        name="Emily",
        specializations=specializations,
    )
    db.session.add(lawyer)
    db.session.commit()
    return lawyer
