from datetime import datetime

from flask import request
from flask_restful import Resource

# from flask_jwt_extended import jwt_required
from sqlalchemy import exc

from calendarapi.api.schemas import AppointmentSchema, VisitorSchema
from calendarapi.extensions import db, ma
from calendarapi.models import (
    Visitor,
    Appointment,
    Schedule,
    Lawyer,
    Specialization,
    City,
)
from calendarapi.services.send_email import send_email


class AppointmentResource(Resource):
    """
    Appointment Resource
    ---
    post:
      tags:
        - Calendar
      summary: Create a new appointment.
      description: Create a new appointment by providing visitor and appointment data in the request body.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                visitor:
                  type: object
                  required:
                    - name
                    - surname
                    - email
                    - phone_number
                    - is_beneficiary
                  properties:
                    name:
                      type: string
                    surname:
                      type: string
                    email:
                      type: string
                    phone_number:
                      type: string
                    is_beneficiary:
                      type: boolean
                appointment:
                  type: object
                  required:
                    - city_id
                    - specialization_id
                    - lawyer_id
                    - appointment_date
                    - appointment_time
                  properties:
                    city_id:
                      type: integer
                    specialization_id:
                      type: integer
                    lawyer_id:
                      type: integer
                    appointment_date:
                      type: string
                      format: date
                    appointment_time:
                      type: string
                      format: time
      responses:
        201:
          description: Appointment created successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        400:
          description: Bad request.
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        500:
          description: Internal server error.
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """

    # method_decorators = [jwt_required()]
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
        visitor = Visitor.query.filter(
            (Visitor.email == kwargs["email"])
            | (Visitor.phone_number == kwargs["phone_number"])
        ).first()
        if visitor:
            [setattr(visitor, key, value) for key, value in kwargs.items()]
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
            validated_visitor_data: Visitor = self.visitor_schema.load(visitor_data)
            validated_appointment_data: Appointment = self.appointment_schema.load(
                {
                    "city": str(
                        db.session.query(City)
                        .filter(City.id == appointment_data.get("city_id"))
                        .one_or_none()
                    ),
                    "specialization": str(
                        db.session.query(Specialization)
                        .filter(
                            Specialization.id
                            == appointment_data.get("specialization_id")
                        )
                        .one_or_none() or "Не вказано"
                    ),
                    "lawyer": str(
                        db.session.query(Lawyer)
                        .filter(Lawyer.id == appointment_data.get("lawyer_id"))
                        .one_or_none()
                    ),
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
            appointment = Appointment(visitor=str(existing_visitor), **appointment_data)
            db.session.add(appointment)
            lawyer_schedule.time = [str(t) for t in lawyer_schedule.time]
            lawyer_schedule.time.remove(
                str(datetime.strptime(appointment_time, "%H:%M").time())
            )
            db.session.commit()
            send_email(
                visitor_name=existing_visitor.name,
                visitor_surname=existing_visitor.surname,
                visitor_email=existing_visitor.email,
                visitor_phone_number=existing_visitor.phone_number,
                appointment_date=appointment.appointment_date,
                appointment_time=str(appointment.appointment_time)[:-3],
                lawyer_name=appointment.lawyer,
                specialization_name=appointment.specialization,
            )
            return {"message": "Appointment created successfully"}, 201

        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"An error occurred while creating the appointment: {str(e)}"
            }, 500
