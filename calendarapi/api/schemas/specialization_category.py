from calendarapi.models import Specialization
from calendarapi.extensions import fm, db
from marshmallow_sqlalchemy.fields import Nested


class SpecializationSchema(fm.SQLAlchemyAutoSchema):
    lawyers = Nested("LawyerSchema", many=True, exclude=("id",))

    class Meta:
        model = Specialization
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
