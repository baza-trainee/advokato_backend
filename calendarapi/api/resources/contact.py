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

            data = {contact.contact_type: contact.value for contact in contacts}
            output_data = [
                {
                    "contacts": [
                        {"phone": data.pop("phone")},
                        {"mail": data.pop("mail")},
                    ],
                    "social": [{"title": k, "url": v} for k, v in data.items()],
                }
            ]
            cities_data = [
                {
                    "id": city.id,
                    "city_name": city.city_name,
                    "address": city.address,
                    "coords": {"lat": city.latitude, "lng": city.longitude},
                }
                for city in cities
            ]
            return {"contacts": output_data, "cities": cities_data}, 200
        except Exception as e:
            return {"message": f"Internal Server Error. {str(e)}"}, 500
