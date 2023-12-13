from typing import List

from flask import request
from flask_restful import Resource

from calendarapi.api.schemas import LawyerSchema
from calendarapi.extensions import db
from calendarapi.models import Lawyer


class LawyersListResource(Resource):
    """
    Lawyers List Resource

    ---
    get:
      tags:
        - Calendar
      summary: Get a list of lawyers.
      description: Get a list of lawyers.
      parameters:
        - name: specialization_id
          in: query
          description: ID of the specialization the lawyers should have.
          required: false
          schema:
            type: integer
      responses:
        200:
          description: List of lawyers
          content:
            application/json:
              example:
                - id: 1
                  name: John Doe
                - id: 2
                  name: Jane Smith
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: The ID of the lawyer.
                    name:
                      type: string
                      description: The name of the lawyer.
        404:
          description: No lawyers found
    """

    lawyer_schema: LawyerSchema = LawyerSchema()

    def get(self):
        specialization_id = request.args.get("specialization_id")

        query = db.session.query(Lawyer.id, Lawyer.name).filter(Lawyer.schedules.any())

        if specialization_id:
            query = query.filter(Lawyer.specializations.any(id=specialization_id))

        lawyers: List[Lawyer] = query.order_by("id").all()
        return self.lawyer_schema.dump(lawyers, many=True), 200
