from flask_restful import Resource, request
# from flask_jwt_extended import jwt_required

from calendarapi.api.schemas import SpecializationSchema
from calendarapi.extensions import db
from calendarapi.models import Specialization, Lawyer


class SpecializationListResource(Resource):
    """
    Specialization Resource

    ---
    get:
      tags:
        - Specialization
      summary: Get a list of specializations.
      description: Get a list of specializations.
      parameters:
        - in: query
          name: city_id
          required: true
          type: integer
          description: "City ID for filtering specializations"
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
        400:
          description: "City ID is required"
    """

    # method_decorators = [jwt_required()]
    specialization_schema: SpecializationSchema = SpecializationSchema()

    def get(self):
        city_id = request.args.get("city_id")

        if not city_id:
            return {"message": "City ID is required"}, 400

        specializations = (
            db.session.query(Specialization.specialization_name, Specialization.id)
            .join(Lawyer.specializations)
            .filter(Lawyer.cities.any(id=city_id))
            .distinct()
            .all()
        )
        return self.specialization_schema.dump(specializations, many=True), 200
