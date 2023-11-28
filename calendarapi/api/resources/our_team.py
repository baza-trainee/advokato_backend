from typing import List

from flask_restful import Resource

# from flask_jwt_extended import jwt_required

from calendarapi.api.schemas import OurTeamSchema
from calendarapi.extensions import db
from calendarapi.models import OurTeam


class OurTeamResource(Resource):
    """
    Our Team Resource

    ---
    get:
      tags:
        - Website content
      summary: Get a list of lawyers.
      description: Get a list of lawyers.
      responses:
        200:
          description: List of lawyers
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
                    photo_path:
                      type: string
                    description:
                      type: string
        404:
          description: No lawyers found.
    """

    # method_decorators = [jwt_required()]
    city_schema: OurTeamSchema = OurTeamSchema()

    def get(self):
        cities: List[OurTeam] = db.session.query(OurTeam).all()
        return self.city_schema.dump(cities, many=True), 200
