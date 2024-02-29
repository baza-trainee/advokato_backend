from typing import List
import json

from flask import url_for, testing
from factory import Factory
from flask_sqlalchemy import SQLAlchemy

from calendarapi.models import Lawyer, Specialization


def test_get_list_of_lawyers(
    client: testing.FlaskClient,
    lawyers_factory: Factory,
    specialization_factory: Factory,
    db: SQLAlchemy,
    city_factory: Factory,
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

    lawyers_list: List[Lawyer] = lawyers_factory.create_batch(2)
    specs_list: List[Specialization] = specialization_factory.create_batch(1)
    city = city_factory.create()
    for lawyer in lawyers_list:
        lawyer.specializations = specs_list
        lawyer.cities = [city]
        db.session.add(lawyer)
        db.session.commit()

    response = client.get(url_for("api.lawyers", specialization_id=1))
    assert response.status_code == 400
    assert response.get_json()["message"] == "City ID is required"

    response = client.get(url_for("api.lawyers", city_id=1))
    assert response.status_code == 400
    assert response.get_json()["message"] == "Specialization ID is required"

    response = client.get(url_for("api.lawyers", city_id=1, specialization_id=1))
    assert response.status_code == 200
    data: List[Lawyer] = json.loads(response.data.decode("utf-8"))
    assert len(data) == len(lawyers_list)

    for lawyer in data:
        for specialization in lawyer["specializations"]:
            assert specialization["specialization_name"] in specialization_example_list

    for response_lawyer, factory_lawyer in zip(data, lawyers_list):
        assert response_lawyer["name"] == factory_lawyer.name
        assert response_lawyer["lawyer_mail"] == factory_lawyer.lawyer_mail
