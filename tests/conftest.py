import json
from typing import Dict
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
from dotenv import load_dotenv
from datetime import date
from calendarapi.models import User
from calendarapi.app import create_app
from calendarapi.extensions import db as _db
from pytest_factoryboy import register
from tests.factories import UserFactory
from calendarapi.app import init_celery
from flask.testing import FlaskClient


register(UserFactory)


@pytest.fixture(scope="session")
def app() -> Flask:
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
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
