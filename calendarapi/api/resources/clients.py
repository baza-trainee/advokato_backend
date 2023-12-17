from typing import List

from flask_restful import Resource

from calendarapi.api.schemas import ClientSchema

# from calendarapi.config import DAY
from calendarapi.extensions import (
    db,
    # cache,
)
from calendarapi.models import Client


class ClientResource(Resource):
    """
    Client Resource

    ---
    get:
      tags:
        - Website content
      summary: Get a list of clients with photo_path and link.
      description: Get a list of clients with photo_path and link.
      responses:
        200:
          description: List of clients
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
                    link:
                      type: string
        404:
          description: No clients found.
    """

    client_schema: ClientSchema = ClientSchema()

    # @cache.cached(key_prefix="client_list", timeout=DAY)
    def get(self):
        clients: List[Client] = db.session.query(Client).all()
        return self.client_schema.dump(clients, many=True), 200
