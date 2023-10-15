from calendarapi.models import Appointment
from calendarapi.extensions import db, fm, ma


time_pattern = r"^(0?[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"


class AppointmentSchema(fm.SQLAlchemyAutoSchema):
    specialization_id = ma.fields.Integer(
        required=True, validate=ma.fields.validate.Range(min=1)
    )
    lawyer_id = ma.fields.Integer(
        required=True, validate=ma.fields.validate.Range(min=1)
    )
    appointment_date = ma.fields.Date(required=True, format="%Y-%m-%d")
    appointment_time = ma.fields.String(
        required=True,
        validate=ma.fields.validate.Regexp(
            time_pattern, error="time format should be 'HH:MM'"
        ),
    )

    class Meta:
        model = Appointment
        exclude = ["id", "visitor_id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
