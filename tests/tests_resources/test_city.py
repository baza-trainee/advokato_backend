from typing import List

from flask import url_for, testing
from factory import Factory
from flask_sqlalchemy import SQLAlchemy

from calendarapi.models import City


def test_get_all_cities(
    client: testing.FlaskClient, city_factory: Factory, db: SQLAlchemy
):
    response = client.get(url_for("api.cities"))
    answer: List[dict] = response.get_json()
    assert response.status_code == 200
    assert len(answer) == 0

    cities: List[City] = city_factory.create_batch(10)
    db.session.add_all(cities)
    db.session.commit()

    response = client.get(url_for("api.cities"))
    answer: List[dict] = response.get_json()
    assert len(answer) == len(cities)
