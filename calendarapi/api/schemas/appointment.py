from calendarapi.models import Appointment
from calendarapi.extensions import db, fm


class AppointmentSchema(fm.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
