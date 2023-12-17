from flask_restful import Resource

from calendarapi.models import Contact, City
from calendarapi.extensions import (
    db,
    # cache,
)

# from calendarapi.config import DAY


class ContactResource(Resource):
    # @cache.cached(key_prefix="contact_list", timeout=DAY)
    def get(self):
        try:
            contacts = db.session.query(Contact).all()
            cities = db.session.query(City).all()
            contacts_data = [
                {
                    contact.contact_type: contact.value,
                }
                for contact in contacts
            ]

            cities_data = [
                {
                    "id": city.id,
                    "city_name": city.city_name,
                    "address": city.address,
                }
                for city in cities
            ]
            return {"contacts": contacts_data, "cities": cities_data}, 200
        except Exception as e:
            return {"message": "Internal Server Error"}, 500
