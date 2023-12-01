from flask_restful import Resource

from calendarapi.extensions import db
from calendarapi.models import Contact, City


class ContactResource(Resource):
    """
    Contact Resource

    ---
    get:
      tags:
        - Website content
      summary: Get a list of contacts and cities.
      description: Get a list of contacts and cities.
      responses:
        200:
          description: List of contacts and cities.
          content:
            application/json:
              schema:
                type: object
                properties:
                  contacts:
                    type: array
                    items:
                      type: object
                      properties:
                        contact_type:
                          type: string
                  cities:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        city_name:
                          type: string
                        address:
                          type: string

        400:
          description: "Bad Request"
    """

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
