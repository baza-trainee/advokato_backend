from typing import List

from flask_restful import Resource
from flask import request

# from flask_jwt_extended import jwt_required

from calendarapi.api.schemas import ClientSchema
from calendarapi.extensions import db
from calendarapi.models import Client


class ClientResource(Resource):
    """
    Client Resource

    ---
    get:
      tags:
        - Clients
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

    # method_decorators = [jwt_required()]
    client_schema: ClientSchema = ClientSchema()

    def get(self):
        clients: List[Client] = db.session.query(Client).all()
        return self.client_schema.dump(clients, many=True), 200
