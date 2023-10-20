import json
from typing import List

from flask import url_for, testing
from factory import Factory
from flask_sqlalchemy import SQLAlchemy

from calendarapi.models import Lawyer, Specialization


def test_get_all_specialization(
    client: testing.FlaskClient,
    lawyers_factory: Factory,
    specialization_factory: Factory,
    db: SQLAlchemy,
    city_factory: Factory,
):
    lawyers_list: List[Lawyer] = lawyers_factory.create_batch(2)
    specs_list: List[Specialization] = specialization_factory.create_batch(2)
    city = city_factory.create()
    for lawyer in lawyers_list:
        lawyer.specializations = specs_list
        lawyer.cities = [city]
        db.session.add(lawyer)
        db.session.commit()

    response = client.get(url_for("api.specialization", city_id=1))
    assert response.status_code == 200

    data: List[Specialization] = json.loads(response.data.decode("utf-8"))
    assert len(data) == len(specs_list)
