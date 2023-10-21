from typing import List
from factory import Factory
from flask_sqlalchemy import SQLAlchemy

from calendarapi.models import Lawyer, Specialization


def test_get_list_of_lawyers(
    lawyers_factory: Factory,
    specialization_factory: Factory,
    db: SQLAlchemy,
    city_factory: Factory,
):
    lawyers_list: List[Lawyer] = lawyers_factory.create_batch(5)
    specs_list: List[Specialization] = specialization_factory.create_batch(1)
    city = city_factory.create()
    for lawyer in lawyers_list:
        lawyer.specializations = specs_list
        lawyer.cities = [city]
        db.session.add(lawyer)
        db.session.commit()

    retrieved_lawyer = Lawyer.query.get(5)

    assert retrieved_lawyer.name == lawyers_list[4].name
    assert retrieved_lawyer.id == 5
