from typing import List

from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError

from calendarapi.api.schemas import CitySchema
from calendarapi.extensions import db, ma
from calendarapi.models import City, Lawyer


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
    post:
      tags:
        - City
      summary: Create a new city.
      description: Create a new city.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CitySchema'
      responses:
        201:
          description: City created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitySchema'
        400:
          description: Bad request, validation error in city data
    """

    city_schema: CitySchema = CitySchema()

    def get(self):
        cities: List[City] = db.session.query(City).all()
        return self.city_schema.dump(cities, many=True), 200

    def post(self):
        try:
            city: City = self.city_schema.load(request.json, session=db.session)
        except ma.ValidationError as e:
            return {"message": str(e)}, 400

        try:
            db.session.add(city)
            db.session.commit()
            return self.city_schema.dump(city), 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Error adding city"}, 500


class CityResource(Resource):
    """
    City Resource

    ---
    delete:
      tags:
        - City
      summary: Delete a city.
      description: Delete a city.
      parameters:
        - name: city_id
          in: path
          required: true
          type: integer
          description: ID of the city to delete
      responses:
        204:
          description: City deleted successfully
        400:
          description: Cannot delete city, as there are lawyers associated with it.
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                  lawyer_names:
                    type: array
                    items:
                      type: string
        404:
          description: City not found
    """

    # @jwt_required()
    def delete(self, city_id: int):
        city: City = db.session.query(City).filter_by(id=city_id).first()
        if city is None:
            return {"message": "City not found"}, 404

        lawyers: List[Lawyer] = (
            db.session.query(Lawyer).filter_by(city_id=city_id).all()
        )
        if lawyers:
            return {
                "message": "Cannot delete city, as there are lawyers associated with it.",
                "lawyer_names": [lawyer.name for lawyer in lawyers],
            }, 400

        db.session.delete(city)
        db.session.commit()
        return "", 204
