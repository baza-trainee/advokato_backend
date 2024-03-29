from typing import List
from flask import url_for, testing
from factory import Factory
from flask_sqlalchemy import SQLAlchemy
from calendarapi.models import Lawyer


def test_get(
    client: testing.FlaskClient,
    schedule_factory: Factory,
    lawyers_factory: Factory,
    db: SQLAlchemy,
):
    lawyers_list: List[Lawyer] = lawyers_factory.create_batch(10)
    schedules = schedule_factory.create_batch(8)

    db.session.add_all(lawyers_list)
    db.session.flush()

    response = client.get(url_for("api.schedule", lawyer_id=1))
    assert response.status_code == 404
    assert (
        response.get_json()["message"] == "No schedule found for the specified lawyer"
    )

    i = 0
    for schedule in schedules:
        i += 1
        schedule.lawyer_id = i
        db.session.add(schedule)

    db.session.commit()

    response = client.get(url_for("api.schedule"))
    assert response.status_code == 400
    assert response.get_json()["message"] == "Lawyer ID is required"

    response = client.get(url_for("api.schedule", lawyer_id=1))
    assert response.status_code == 200
