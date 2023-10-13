from typing import List

from flask_restful import Resource
from sqlalchemy.orm import joinedload

from calendarapi.api.schemas import SpecializationSchema
from calendarapi.extensions import db
from calendarapi.models import Specialization, Lawyer


class SpecializationListResource(Resource):
    """
    Specialization Resource

    ---
    get:
      tags:
        - Lawyer
      summary: Get a list of specializations.
      description: Get a list of specializations.
      responses:
        200:
          description: List of specializations.
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    question:
                      type: string
        404:
          description: No specialization found.
    """

    specialization_schema: SpecializationSchema = SpecializationSchema()

    def get(self):
        specializations: List[Specialization] = (
            db.session.query(Specialization)
            .options(
                joinedload(Specialization.lawyers).joinedload(Lawyer.specializations)
            )
            .all()
        )
        return self.specialization_schema.dump(specializations, many=True), 200
