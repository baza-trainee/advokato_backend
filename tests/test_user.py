from typing import Dict
from flask import url_for
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from factory import Factory

from calendarapi.extensions import pwd_context
from calendarapi.models import User


def test_get_user(
    client: FlaskClient, db: SQLAlchemy, user: User, admin_headers: Dict[str, str]
):
    user_url = url_for("api.user_by_id", user_id="100000")
    response = client.get(user_url, headers=admin_headers)
    assert response.status_code == 404

    db.session.add(user)
    db.session.commit()

    user_url = url_for("api.user_by_id", user_id=user.id)
    response = client.get(user_url, headers=admin_headers)
    assert response.status_code == 200

    data: dict = response.get_json()["user"]
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["active"] == user.active


def test_put_user(
    client: FlaskClient, db: SQLAlchemy, user: User, admin_headers: Dict[str, str]
):
    user_url = url_for("api.user_by_id", user_id="100000")
    response = client.put(user_url, headers=admin_headers)
    assert response.status_code == 404

    db.session.add(user)
    db.session.commit()

    data = {"username": "updated", "password": "new_password"}

    user_url = url_for("api.user_by_id", user_id=user.id)
    response = client.put(user_url, json=data, headers=admin_headers)
    assert response.status_code == 200

    data: dict = response.get_json()["user"]
    assert data["username"] == "updated"
    assert data["email"] == user.email
    assert data["active"] == user.active

    db.session.refresh(user)
    assert pwd_context.verify("new_password", user.password)


def test_delete_user(
    client: FlaskClient, db: SQLAlchemy, user: User, admin_headers: Dict[str, str]
):
    user_url = url_for("api.user_by_id", user_id="100000")
    response = client.delete(user_url, headers=admin_headers)
    assert response.status_code == 404

    db.session.add(user)
    db.session.commit()

    user_url = url_for("api.user_by_id", user_id=user.id)
    response = client.delete(user_url, headers=admin_headers)
    assert response.status_code == 200
    assert db.session.query(User).filter_by(id=user.id).first() is None


def test_create_user(
    client: FlaskClient, db: SQLAlchemy, admin_headers: Dict[str, str]
):
    users_url = url_for("api.users")
    data = {"username": "created"}
    response = client.post(users_url, json=data, headers=admin_headers)
    assert response.status_code == 400

    data["password"] = "admin"
    data["email"] = "create@mail.com"

    response = client.post(users_url, json=data, headers=admin_headers)
    assert response.status_code == 201

    data: dict = response.get_json()
    user = db.session.query(User).filter_by(id=data["user"]["id"]).first()

    assert user.username == "created"
    assert user.email == "create@mail.com"


def test_get_all_user(
    client: FlaskClient,
    db: SQLAlchemy,
    user_factory: Factory,
    admin_headers: Dict[str, str],
):
    users_url = url_for("api.users")
    users = user_factory.create_batch(30)

    db.session.add_all(users)
    db.session.commit()

    repsponse = client.get(users_url, headers=admin_headers)
    assert repsponse.status_code == 200
    results: dict = repsponse.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results["results"])
