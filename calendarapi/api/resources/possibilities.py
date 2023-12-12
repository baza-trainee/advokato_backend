from typing import List

from flask_restful import Resource

from calendarapi.api.schemas import PossibilitiesSchema
from calendarapi.extensions import db
from calendarapi.models import Possibilities


class PossibilitiesResource(Resource):
    """
    Possibilities Resource

    ---
    get:
      tags:
        - Website content
      summary: Get a list of possibilities.
      description: Get a list of possibilities.
      responses:
        200:
          description: List of possibilities
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    title:
                      type: string
                    photo_path:
                      type: string
                    short_text:
                      type: string
                    description:
                      type: string
        404:
          description: No possibilities found.
    """

    possibilities_schema: PossibilitiesSchema = PossibilitiesSchema()

    def get(self):
        possibilities: List[Possibilities] = db.session.query(Possibilities).all()
        return self.possibilities_schema.dump(possibilities, many=True), 200
