from typing import List

from flask_restful import Resource

from calendarapi.api.schemas import ProBonoSchema
# from calendarapi.config import DAY
from calendarapi.extensions import (
    db,
    # cache,
)
from calendarapi.models import ProBono


class ProBonoResource(Resource):
    """
    Pro Bono Resource

    ---
    get:
      tags:
        - Website content
      summary: Get a list of Pro Bono.
      description: Get a list of Pro Bono.
      responses:
        200:
          description: List of Pro Bono
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    photo_path:
                      type: string
                    description:
                      type: string
        404:
          description: No data found.
    """

    city_schema: ProBonoSchema = ProBonoSchema()

    # @cache.cached(key_prefix="pro_bono", timeout=DAY)
    def get(self):
        data_list: List[ProBono] = db.session.query(ProBono).all()
        return self.city_schema.dump(data_list, many=True), 200
