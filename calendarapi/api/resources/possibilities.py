from typing import List

from flask_restful import Resource
from sqlalchemy import exc

from calendarapi.api.schemas import PossibilitiesSchema

# from calendarapi.config import DAY
from calendarapi.models import Possibilities
from calendarapi.extensions import (
    db,
    # cache,
)


class PossibilitiesResource(Resource):
    possibilities_schema: PossibilitiesSchema = PossibilitiesSchema()

    # @cache.cached(key_prefix="possibilities", timeout=DAY)
    def get(self):
        try:
            possibilities: List[Possibilities] = (
                db.session.query(Possibilities).order_by("id").all()
            )
        except exc.SQLAlchemyError as e:
            return {"error": f"Database error: {str(e)}"}, 500
        return self.possibilities_schema.dump(possibilities, many=True), 200
