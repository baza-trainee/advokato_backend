from calendarapi.models import Appointment
from calendarapi.extensions import ma, db


class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
