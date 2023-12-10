from typing import List

from flask_restful import Resource

from calendarapi.api.schemas import CitySchema
from calendarapi.config import DAY
from calendarapi.extensions import db, cache
from calendarapi.models import City


class CityListResource(Resource):
    """
    City Resource

    ---
    get:
      tags:
        - Calendar
      summary: Get a list of cities.
      description: Get a list of cities.
      responses:
        200:
          description: List of cities
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
        404:
          description: No city found.
    """

    city_schema: CitySchema = CitySchema()

    @cache.cached(key_prefix="city_list", timeout=DAY)
    def get(self):
        cities: List[City] = db.session.query(City).all()
        return self.city_schema.dump(cities, many=True), 200
