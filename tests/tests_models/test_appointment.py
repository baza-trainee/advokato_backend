from flask_sqlalchemy import SQLAlchemy
from calendarapi.models import Appointment
from factory import Factory


def test_create_and_retrieve_appointment(
    db: SQLAlchemy,
    lawyers_factory: Factory,
    specialization_factory: Factory,
    visitor_factory: Factory,
    city_factory: Factory,
):
    visitor = visitor_factory.create()
    lawyer = lawyers_factory.create()
    specs = specialization_factory.create()
    city = city_factory.create()
    lawyer.specializations = [specs]
    lawyer.cities = [city]
    db.session.add(lawyer)
    db.session.commit()

    db.session.add(visitor)
    db.session.commit()

    appointment = Appointment(
        visitor_id=1,
        specialization_id=1,
        lawyer_id=1,
        appointment_date="2023-10-20",
        appointment_time="10:00:00",
    )

    db.session.add(appointment)
    db.session.commit()

    retrieved_appointment = Appointment.query.get(1)

    assert retrieved_appointment.visitor_id == 1
    assert retrieved_appointment.specialization_id == 1
    assert retrieved_appointment.lawyer_id == 1
    assert str(retrieved_appointment.appointment_date) == "2023-10-20"
    assert str(retrieved_appointment.appointment_time) == "10:00:00"
    expected_repr = f"Appointment: {retrieved_appointment.visitor_id}. Question: {retrieved_appointment.specialization_id}"
    assert repr(appointment), expected_repr
