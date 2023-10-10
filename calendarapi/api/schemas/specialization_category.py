from calendarapi.models import SpecializationCategory
from calendarapi.extensions import ma, db
from marshmallow_sqlalchemy.fields import Nested


class SpecializationSchema(ma.SQLAlchemyAutoSchema):
    lawyers = Nested("LawyerSchema", many=True, exclude=("id",))

    class Meta:
        model = SpecializationCategory
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
