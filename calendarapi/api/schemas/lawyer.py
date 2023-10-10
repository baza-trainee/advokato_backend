from calendarapi.models import Lawyer
from calendarapi.extensions import ma, db


class LawyerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lawyer
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
