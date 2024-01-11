from typing import List

from flask_restful import Resource

from calendarapi.api.schemas import ProBonoSchema
from sqlalchemy import exc

from calendarapi.config import DAY
from calendarapi.extensions import (
    db,
    cache,
)
from calendarapi.models import ProBono


class ProBonoResource(Resource):
    pro_bono: ProBonoSchema = ProBonoSchema()

    @cache.cached(key_prefix="pro_bono", timeout=DAY)
    def get(self):
        try:
            data: List[ProBono] = db.session.query(ProBono).order_by("id").all()
        except exc.SQLAlchemyError as e:
            return {"error": f"Database error: {str(e)}"}, 500
        return self.pro_bono.dump(data, many=True), 200
