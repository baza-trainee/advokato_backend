from smtplib import SMTPException

from flask_restful import Resource, request
from sqlalchemy import exc
from marshmallow import ValidationError

from calendarapi.api.schemas.visitor import VisitorSchema
from calendarapi.services.send_email import send_email
from calendarapi.models import Visitor
from calendarapi.extensions import db


class FeedbackResource(Resource):
    visitor_schema = VisitorSchema()

    def find_or_create_visitor(self, **kwargs) -> Visitor:
        try:
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
                return
            new_visitor = Visitor(**kwargs)
            db.session.add(new_visitor)
            db.session.commit()
            return
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database error: {str(e)}"}, 500

    def validate_message_length(self, message):
        if len(message) > 2000:
            raise ValidationError("Message length cannot exceed 2000 characters.")

    def post(self):
        if not request.is_json:
            return {"error": "Invalid JSON"}, 400
        data = request.get_json()
        try:
            self.validate_message_length(data.get("message", ""))
            validated_visitor_data: Visitor = self.visitor_schema.load(
                {
                    "email": data.get("email"),
                    "name": data.get("name"),
                    "phone_number": data.get("phone_number"),
                }
            )
        except ValidationError as e:
            return {"error": str(e)}, 400
        self.find_or_create_visitor(**self.visitor_schema.dump(validated_visitor_data))
        try:
            send_email(
                feedback=True,
                visitor_name=data.get("name", "Не вказано"),
                visitor_email=data.get("email", "Не вказана"),
                visitor_phone_number=data.get("phone_number"),
                message=data.get("message"),
            )
        except SMTPException as e:
            return {"error": f"Email sending error: {str(e)}"}, 500
        return {"success": True}, 200
