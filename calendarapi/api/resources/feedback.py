from flask import request
from flask_restful import Resource

from calendarapi.services.send_email import send_email


class FeedbackResource(Resource):
    """
    Feedback Resource

    ---
    post:
      tags:
        - Website content
      summary: Submit feedback.
      description: Submit feedback from users.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Visitor's name.
                mail:
                  type: string
                  format: email
                  description: Visitor's email address.
                phone:
                  type: string
                  description: Visitor's phone number.
                message:
                  type: string
                  description: Feedback message.
              required:
                - name
                - mail
                - message
      responses:
        200:
          description: Feedback submitted successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    description: Indicates if the feedback was successfully submitted.
        400:
          description: Bad Request. Invalid JSON or missing required fields.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Error message.
    """

    def post(self):
        if not request.is_json:
            return {"error": "Invalid JSON"}, 400
        data = request.get_json()
        required_fields = ["name", "mail", "message"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400
        send_email.delay(
            feedback=True,
            visitor_name=data["name"],
            visitor_email=data["mail"],
            visitor_phone_number=data["phone"],
            message=data["message"],
        )
        return {"success": True}, 200
