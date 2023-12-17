from calendarapi.models import Lawyer
from calendarapi.extensions import fm, db, ma
from calendarapi.commons.exeptions import INVALID_EMAIL


class LawyerSchema(fm.SQLAlchemyAutoSchema):
    city_id = ma.fields.Int(validate=ma.fields.validate.Range(min=1, max=3))
    lawyer_mail = ma.fields.String(
        required=True,
        validate=[
            ma.fields.validate.Email(error=INVALID_EMAIL),
        ],
    )
    name = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=100)
    )
    specializations = ma.fields.List(
        ma.fields.Nested("SpecializationSchema", only=("specialization_name",))
    )

    class Meta:
        model = Lawyer
        include_fk = True
        load_instance = True
        sqla_session = db.session
