from flask_sqlalchemy import SQLAlchemy
from calendarapi.models import City


def test_create_and_retrieve_city(
    db: SQLAlchemy,
):
    city = City(city_name="Test City")

    db.session.add(city)
    db.session.commit()

    retrieved_city = City.query.get(1)

    assert retrieved_city.city_name == "Test City"
    assert retrieved_city.id == 1

    assert repr(city), retrieved_city.city_name
