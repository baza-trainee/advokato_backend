from datetime import datetime

from flask_restful import Resource, request
from sqlalchemy import exc

from calendarapi.api.schemas import AppointmentSchema, VisitorSchema
from calendarapi.services.send_email import send_email
from calendarapi.extensions import db, ma
from calendarapi.models import (
    Visitor,
    Appointment,
    Schedule,
    Lawyer,
    Specialization,
)


class AppointmentResource(Resource):
    visitor_schema = VisitorSchema()
    appointment_schema = AppointmentSchema()

    def get_lawyer_schedule(self, lawyer_id: int, date: str) -> Schedule:
        lawyer_schedule = Schedule.query.filter_by(
            lawyer_id=lawyer_id, date=date
        ).first()
        return lawyer_schedule

    def is_time_available(
        self, lawyer_schedule: Schedule, date: str, time: str
    ) -> bool:
        appointment_time = datetime.strptime(time, "%H:%M").time()
        if lawyer_schedule.date == date and appointment_time in lawyer_schedule.time:
            return True
        return False

    def find_or_create_visitor(self, **kwargs) -> Visitor:
        phone_number = kwargs.get("phone_number")
        email = kwargs.get("email")

        if email is not None:
            visitor = Visitor.query.filter(
                (Visitor.phone_number == phone_number) | (Visitor.email == email)
            ).first()
        else:
            visitor = Visitor.query.filter_by(phone_number=phone_number).first()

        if visitor:
            [setattr(visitor, key, value) for key, value in kwargs.items() if value]
            db.session.commit()
            return visitor
        new_visitor = Visitor(**kwargs)
        db.session.add(new_visitor)
        db.session.flush()
        return new_visitor

    def post(self):
        json_data = request.get_json()
        visitor_data = json_data["visitor"]
        appointment_data = json_data["appointment"]

        try:
            lawyer = (
                db.session.query(Lawyer)
                .filter(Lawyer.id == appointment_data.get("lawyer_id"))
                .one_or_none()
            )
            specialization_id = appointment_data.get("specialization_id")
            if specialization_id is not None and not isinstance(specialization_id, int):
                raise ma.ValidationError(
                    "specialization_id must be an integer or null."
                )

            validated_visitor_data: Visitor = self.visitor_schema.load(visitor_data)
            validated_appointment_data: Appointment = self.appointment_schema.load(
                {
                    "specialization": str(
                        db.session.query(Specialization)
                        .filter(Specialization.id == specialization_id)
                        .one_or_none()
                        or "Не вказано"
                    ),
                    "lawyer": str(lawyer),
                    "appointment_date": appointment_data.get("appointment_date"),
                    "appointment_time": appointment_data.get("appointment_time"),
                }
            )
        except ma.ValidationError as e:
            return {"message": e.messages}, 400
        appointment_date = validated_appointment_data.appointment_date
        appointment_time = validated_appointment_data.appointment_time
        lawyer_schedule = self.get_lawyer_schedule(
            appointment_data.get("lawyer_id"), appointment_date
        )
        appointment_data: dict = self.appointment_schema.dump(
            validated_appointment_data
        )
        visitor_data: dict = self.visitor_schema.dump(validated_visitor_data)
        existing_visitor = self.find_or_create_visitor(**visitor_data)
        if lawyer_schedule is None:
            return {"message": "Date not available for this lawyer"}, 400
        if not self.is_time_available(
            lawyer_schedule, appointment_date, str(appointment_time)
        ):
            return {"message": "Time not available for this lawyer"}, 400

        try:
            appointment = Appointment(
                visitor_id=existing_visitor.id, **appointment_data
            )
            db.session.add(appointment)
            lawyer_schedule.time = [str(t) for t in lawyer_schedule.time]
            lawyer_schedule.time.remove(
                str(datetime.strptime(appointment_time, "%H:%M").time())
            )
            if not lawyer_schedule.time:
                db.session.delete(lawyer_schedule)
            db.session.commit()
            send_email.delay(
                visitor_name=existing_visitor.name,
                visitor_email=existing_visitor.email,
                visitor_phone_number=existing_visitor.phone_number,
                appointment_date=appointment.appointment_date,
                appointment_time=str(appointment.appointment_time)[:-3],
                lawyer_email=lawyer.lawyer_mail,
                lawyer_name=appointment.lawyer,
                specialization_name=appointment.specialization,
            )
            return {"message": "Appointment created successfully"}, 201

        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"An error occurred while creating the appointment: {str(e)}"
            }, 500
