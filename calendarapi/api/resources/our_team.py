from typing import List

from flask_restful import Resource

from calendarapi.api.schemas import OurTeamSchema
from calendarapi.config import DAY
from calendarapi.extensions import db, cache
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

    city_schema: OurTeamSchema = OurTeamSchema()

    @cache.cached(key_prefix="team_list", timeout=DAY)
    def get(self):
        cities: List[OurTeam] = db.session.query(OurTeam).all()
        return self.city_schema.dump(cities, many=True), 200
