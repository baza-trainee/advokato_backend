from typing import List

from flask_restful import Resource
from flask_jwt_extended import jwt_required

from calendarapi.api.schemas import CitySchema
from calendarapi.extensions import db
from calendarapi.models import City


class CityListResource(Resource):
    """
    City Resource

    ---
    get:
      tags:
        - City
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

    method_decorators = [jwt_required()]
    city_schema: CitySchema = CitySchema()

    def get(self):
        cities: List[City] = db.session.query(City).all()
        return self.city_schema.dump(cities, many=True), 200
