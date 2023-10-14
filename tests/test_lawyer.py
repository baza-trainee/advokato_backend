from datetime import date
from typing import Dict, List
import json

from flask import url_for, testing
from factory import Factory
from flask_sqlalchemy import SQLAlchemy

from calendarapi.models import Lawyer, City, Specialization


def test_get_list_of_lawyers(
    client: testing.FlaskClient,
    lawyer_factory: Factory,
    specialization_factory: Factory,
    db: SQLAlchemy,
):
    specialization_example_list = [
        "Цивільна",
        "Адміністративна",
        "Кримінальна",
        "Сімейна",
        "Військовий",
        "Зруйноване майно",
        "Порушення прав людини",
    ]
    lawyers_list: List[Lawyer] = lawyer_factory.create_batch(2)
    specs_list: List[Specialization] = specialization_factory.create_batch(2)

    for lawyer in lawyers_list:
        lawyer.specializations = specs_list

    db.session.add_all(lawyers_list)
    response = client.get(url_for("api.lawyers"))

    assert response.status_code == 200
    data: List[Lawyer] = json.loads(response.data.decode("utf-8"))
    assert len(data) == len(lawyers_list)

    for lawyer in data:
        for specialization in lawyer["specializations"]:
            assert specialization["specialization_name"] in specialization_example_list

    for response_lawyer, factory_lawyer in zip(data, lawyers_list):
        assert response_lawyer["name"] == factory_lawyer.name
        assert response_lawyer["surname"] == factory_lawyer.surname
        assert response_lawyer["lawyer_mail"] == factory_lawyer.lawyer_mail


def test_post_create_lawyer(
    client: testing.FlaskClient,
    db: SQLAlchemy,
    admin_headers: Dict[str, str],
):
    lawyer_to_create = {
        "name": "David",
        "surname": "Johnson",
        "lawyer_mail": "david@example.com",
        "city_id": 2,
    }
    response = client.post(
        url_for("api.lawyers"), json=lawyer_to_create, headers=admin_headers
    )
    assert response.status_code == 201

    answer: dict = response.get_json()
    assert answer["message"] == "Lawyer created successfully"

    lawyer_in_db: Lawyer = (
        db.session.query(Lawyer)
        .filter_by(lawyer_mail=lawyer_to_create["lawyer_mail"])
        .first()
    )
    assert lawyer_in_db is not None
    assert lawyer_in_db.name == lawyer_to_create["name"]


def test_patch_existing_lawyer(
    client: testing.FlaskClient,
    db: SQLAlchemy,
    lawyer: Lawyer,
    admin_headers: Dict[str, str],
):
    updated_data = {
        "name": "testing",
        "surname": "Johnson",
    }
    lawyer_url = url_for("api.lawyer_by_id", lawyer_id=lawyer.id)
    response = client.patch(lawyer_url, json=updated_data, headers=admin_headers)
    assert response.status_code == 200
    updated_lawyer: Lawyer = db.session.query(Lawyer).filter_by(id=lawyer.id).first()
    assert updated_lawyer.name == updated_data["name"]
    assert updated_lawyer.surname == updated_data["surname"]


def test_delete_lawyer(
    client: testing.FlaskClient,
    db: SQLAlchemy,
    lawyer: Lawyer,
    admin_headers: Dict[str, str],
):
    lawyer_url = url_for("api.lawyer_by_id", lawyer_id=123)
    rep = client.delete(lawyer_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(lawyer)
    db.session.commit()

    user_url = url_for("api.lawyer_by_id", lawyer_id=lawyer.id)
    rep = client.delete(user_url, headers=admin_headers)
    assert rep.status_code == 204
    assert db.session.query(Lawyer).filter_by(id=lawyer.id).first() is None
