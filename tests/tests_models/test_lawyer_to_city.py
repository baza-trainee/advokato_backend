from flask_sqlalchemy import SQLAlchemy
from calendarapi.models.layers_to_cities import layersToCities
from factory import Factory


def test_layers_to_cities(
    lawyers_factory: Factory,
    db: SQLAlchemy,
    city_factory: Factory,
):
    lawyers_list = lawyers_factory.create_batch(2)
    city = city_factory.create()
    for lawyer in lawyers_list:
        lawyer.cities = [city]
        db.session.add(lawyer)
        db.session.commit()

    retrieved_layers_to_cities = layersToCities.query.get((1, 1))

    assert retrieved_layers_to_cities.lawyer_id, 1
    assert retrieved_layers_to_cities.city_id, 1
