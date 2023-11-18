from typing import List

from flask import request
from flask_restful import Resource

# from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload

from calendarapi.api.schemas import LawyerSchema
from calendarapi.extensions import db
from calendarapi.models import Lawyer


class LawyersListResource(Resource):
    """
    Lawyers List Resource

    ---
    get:
      tags:
        - Lawyer
      summary: Get a list of lawyers.
      description: Get a list of lawyers.
      parameters:
        - name: city_id
          in: query
          description: ID of the city where the lawyers work.
          required: true
          schema:
            type: integer
        - name: specialization_id
          in: query
          description: ID of the specialization the lawyers should have.
          required: true
          schema:
            type: integer
      responses:
        200:
          description: List of lawyers
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/LawyerSchema'
        404:
          description: No lawyers found
    """

    # method_decorators = [jwt_required()]
    lawyer_schema: LawyerSchema = LawyerSchema()

    def get(self):
        city_id = request.args.get("city_id")
        specialization_id = request.args.get("specialization_id")

        if not city_id:
            return {"message": "City ID is required"}, 400

        if not specialization_id:
            return {"message": "Specialization ID is required"}, 400

        lawyers: List[Lawyer] = (
            db.session.query(Lawyer)
            .options(joinedload(Lawyer.specializations))
            .filter(Lawyer.cities.any(id=city_id))
            .filter(Lawyer.specializations.any(id=specialization_id))
            .all()
        )
        return self.lawyer_schema.dump(lawyers, many=True), 200
