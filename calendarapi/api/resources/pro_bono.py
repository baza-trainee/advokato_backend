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
    pro_bono: ProBonoSchema = ProBonoSchema()

    # @cache.cached(key_prefix="pro_bono", timeout=DAY)
    def get(self):
        data: List[ProBono] = db.session.query(ProBono).all()
        return self.pro_bono.dump(data, many=True), 200
