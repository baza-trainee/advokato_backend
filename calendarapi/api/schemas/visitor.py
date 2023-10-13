from calendarapi.models import Visitor
from calendarapi.extensions import fm, db


class VisitorSchema(fm.SQLAlchemyAutoSchema):
    class Meta:
        model = Visitor
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
