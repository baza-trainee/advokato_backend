from flask import url_for
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from factory import Factory
from typing import List
from calendarapi.models import Lawyer, Specialization, Appointment
from calendarapi.models.visitor import Visitor
from unittest.mock import patch
from calendarapi.api.resources.appointment import AppointmentResource
from calendarapi.models import Schedule


def test_create_appointment_correct(
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
        },
    }

    appointment_wrong_data = {
        "appointment": {
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
        },
    }

    appointment_data_wrong_time = {
        "appointment": {
            "appointment_date": str(schedules[0].date),
            "appointment_time": "8:00",
            "city_id": 1,
            "lawyer_id": schedules[0].lawyer_id,
            "specialization_id": 1,
        },
        "visitor": {
            "email": visitor.email,
            "is_beneficiary": visitor.is_beneficiary,
            "phone_number": "+380961245359",
            "name": visitor.name,
        },
    }

    appointment_data_wrong_date = {
        "appointment": {
            "appointment_date": "2023-01-01",
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

        # Check that the new visitor is in the database
        assert visitor is not None

        # Retrieve the visitor from the database
        retrieved_visitor = (
            db.session.query(Visitor).filter_by(email=visitor.email).first()
        )
        assert retrieved_visitor is not None

        assert retrieved_visitor.name == visitor.name
        assert retrieved_visitor.phone_number == visitor.phone_number
        assert retrieved_visitor.is_beneficiary == visitor.is_beneficiary

        response = client.post(
            url_for("api.appointment"),
            json=appointment_wrong_data,
            content_type="application/json",
        )

        assert response.status_code == 400

        response = client.post(
            url_for("api.appointment"),
            json=appointment_data_wrong_time,
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "Time not available for this lawyer" in response.json["message"]

        response = client.post(
            url_for("api.appointment"),
            json=appointment_data_wrong_date,
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "Date not available for this lawyer" in response.json["message"]


def test_is_time_available_returns_false():
    # Create a lawyer schedule that doesn't have the specified time
    schedule = Schedule(
        lawyer_id=1, date="2023-10-20", time=["08:00", "09:00", "10:00"]
    )
    appointment_resource = AppointmentResource()

    # Test the `is_time_available` method
    result = appointment_resource.is_time_available(schedule, "2023-10-20", "11:00")

    assert result is False
