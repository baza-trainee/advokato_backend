from typing import List

from flask_restful import Resource, request

from calendarapi.api.schemas import LawyerSchema
from calendarapi.extensions import db
from calendarapi.models import Lawyer


class LawyersListResource(Resource):
    lawyer_schema: LawyerSchema = LawyerSchema()

    def get(self):
        specialization_id = request.args.get("specialization_id")

        query = db.session.query(Lawyer.id, Lawyer.name).filter(Lawyer.schedules.any())

        if specialization_id:
            query = query.filter(Lawyer.specializations.any(id=specialization_id))

        lawyers: List[Lawyer] = query.order_by("id").all()
        return self.lawyer_schema.dump(lawyers, many=True), 200
