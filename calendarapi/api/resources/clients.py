from typing import List

from flask_restful import Resource

from calendarapi.api.schemas import ClientSchema
from calendarapi.models import Client

# from calendarapi.config import DAY
from calendarapi.extensions import (
    db,
    # cache,
)


class ClientResource(Resource):
    client_schema: ClientSchema = ClientSchema()

    # @cache.cached(key_prefix="client_list", timeout=DAY)
    def get(self):
        clients: List[Client] = db.session.query(Client).all()
        return self.client_schema.dump(clients, many=True), 200
