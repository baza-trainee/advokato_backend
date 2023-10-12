import json
from typing import List

from flask import url_for, testing
from factory import Factory
from flask_sqlalchemy import SQLAlchemy

from calendarapi.models import Lawyer, Specialization


def test_get_all_specialization(
    client: testing.FlaskClient,
    lawyer_factory: Factory,
    specialization_factory: Factory,
    db: SQLAlchemy,
):
    lawyers_list: List[Lawyer] = lawyer_factory.create_batch(1)
    specs_list: List[Specialization] = specialization_factory.create_batch(2)

    for lawyer in lawyers_list:
        lawyer.specializations = specs_list
    db.session.add_all(lawyers_list)
    db.session.commit()

    response = client.get(url_for("api.specialization"))
    assert response.status_code == 200

    data: List[Specialization] = json.loads(response.data.decode("utf-8"))
    assert len(data) == len(specs_list)
