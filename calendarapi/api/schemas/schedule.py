from calendarapi.models import Schedule
from calendarapi.extensions import fm, db
from marshmallow_sqlalchemy.fields import Nested


class ScheduleSchema(fm.SQLAlchemyAutoSchema):
    lawyers = Nested("LawyerSchema")

    class Meta:
        model = Schedule
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
