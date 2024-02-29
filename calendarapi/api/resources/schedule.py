from datetime import datetime

from flask_restful import Resource, request
from sqlalchemy import and_

from calendarapi.api.schemas import ScheduleSchema
from calendarapi.extensions import db
from calendarapi.models import Schedule


class ScheduleResource(Resource):
    schedule_schema: ScheduleSchema = ScheduleSchema()

    def get(self):
        lawyer_id = request.args.get("lawyer_id")
        if not lawyer_id:
            return {"message": "Lawyer ID is required"}, 400
        current_date = datetime.now().date()
        lawyer_schedule = (
            db.session.query(Schedule)
            .where(and_(Schedule.lawyer_id == lawyer_id, Schedule.date >= current_date))
            .all()
        )
        if not lawyer_schedule:
            return {"message": "No schedule found for the specified lawyer"}, 404
        output = [
            {
                "date": schedule.date,
                "time": [time.strftime("%H:%M") for time in schedule.time],
                "lawyer_id": schedule.lawyer_id,
            }
            for schedule in lawyer_schedule
        ]
        return self.schedule_schema.dump(output, many=True), 200
