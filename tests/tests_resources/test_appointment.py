from flask import url_for
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from factory import Factory
from typing import List
from calendarapi.models import Lawyer, Specialization, Appointment
from unittest.mock import patch


def test_create_appointment(
    client: FlaskClient,
    db: SQLAlchemy,
    lawyers_factory: Factory,
    specialization_factory: Factory,
    visitor_factory: Factory,
    schedule_factory: Factory,
    city_factory: Factory,
):
    visitor = visitor_factory.create()

    lawyers_list: List[Lawyer] = lawyers_factory.create_batch(4)
    specs_list: List[Specialization] = specialization_factory.create_batch(1)
    city = city_factory.create()
    for lawyer in lawyers_list:
        lawyer.specializations = specs_list
        lawyer.cities = [city]
        db.session.add(lawyer)
        db.session.commit()

    schedules = schedule_factory.create_batch(4)
    i = 0
    for schedule in schedules:
        i += 1
        schedule.lawyer_id = i
        db.session.add(schedule)
    db.session.add(visitor)
    db.session.commit()
    appointment_data = {
        "appointment": {
            "appointment_date": str(schedules[0].date),
            "appointment_time": "10:00",
            "city_id": 1,
            "lawyer_id": schedules[0].lawyer_id,
            "specialization_id": 1,
        },
        "visitor": {
            "email": visitor.email,
            "is_beneficiary": visitor.is_beneficiary,
            "phone_number": "+380961245359",
            "name": visitor.name,
            "surname": visitor.surname,
        },
    }
    with patch(
        "calendarapi.api.resources.appointment.send_email.delay"
    ) as mock_send_email:
        mock_send_email.return_value = "Повідомлення відправлено"
        response = client.post(
            url_for("api.appointment"),
            json=appointment_data,
            content_type="application/json",
        )

        assert response.status_code == 201
        assert "Appointment created successfully" in response.json["message"]

        created_appointment = (
            db.session.query(Appointment).filter_by(visitor_id=visitor.id).first()
        )
        assert created_appointment is not None
