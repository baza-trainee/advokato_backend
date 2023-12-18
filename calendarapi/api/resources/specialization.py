from flask_restful import Resource

from calendarapi.api.schemas import SpecializationSchema
from calendarapi.models import Specialization, Lawyer

# from calendarapi.config import DAY
from calendarapi.extensions import (
    db,
    # cache,
)


class SpecializationListResource(Resource):
    specialization_schema: SpecializationSchema = SpecializationSchema()

    def get(self):
        specializations = (
            db.session.query(Specialization.specialization_name, Specialization.id)
            .join(Lawyer.specializations)
            .distinct()
            .order_by("id")
            .all()
        )
        return self.specialization_schema.dump(specializations, many=True), 200


class AllSpecializationsResource(Resource):
    specialization_schema: SpecializationSchema = SpecializationSchema()

    # @cache.cached(key_prefix="specialization_list", timeout=DAY)
    def get(self):
        try:
            all_specializations = db.session.query(Specialization).all()
            return self.specialization_schema.dump(all_specializations, many=True), 200
        except Exception as e:
            return {"message": "Internal Server Error"}, 500
