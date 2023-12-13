from flask_restful import Resource

from calendarapi.api.schemas import SpecializationSchema
from calendarapi.extensions import db
from calendarapi.models import Specialization, Lawyer


class SpecializationListResource(Resource):
    """
    Specialization Resource

    ---
    get:
      tags:
        - Calendar
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
                    specialization_name:
                      type: string
    """

    specialization_schema: SpecializationSchema = SpecializationSchema()

    def get(self):
        specializations = (
            db.session.query(Specialization.specialization_name, Specialization.id)
            .join(Lawyer.specializations)
            .distinct()
            .order_by("id")
            .all()
        )
        return self.specialization_schema.dump(specializations, many=True), 200


class AllSpecializationsResource(Resource):
    """
    All Specializations Resource

    ---
    get:
      tags:
        - Website content
      summary: Get a list of all specializations with photos and descriptions.
      description: Get a list of all specializations including their photos and descriptions.
      responses:
        200:
          description: List of all specializations with photos and descriptions.
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    specialization_name:
                      type: string
                    specialization_description:
                      type: string
                    specialization_photo:
                      type: string
                      format: uri

        400:
          description: "Bad Request"
    """

    specialization_schema: SpecializationSchema = SpecializationSchema()

    def get(self):
        try:
            all_specializations = db.session.query(
                Specialization.id,
                Specialization.specialization_name,
                Specialization.specialization_description,
                Specialization.specialization_photo,
            ).all()
            return self.specialization_schema.dump(all_specializations, many=True), 200
        except Exception as e:
            return {"message": "Internal Server Error"}, 500
