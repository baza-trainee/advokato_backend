from calendarapi.models import Lawyer
from calendarapi.extensions import fm, db, ma


class LawyerSchema(fm.SQLAlchemyAutoSchema):
    city_id = ma.fields.Int(validate=ma.fields.validate.Range(min=1, max=3))
    lawyer_mail = ma.fields.String(required=True, validate=ma.fields.validate.Email())
    name = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=3, max=30)
    )
    surname = ma.fields.String(validate=ma.fields.validate.Length(min=3, max=30))
    specializations = ma.fields.List(
        ma.fields.Nested("SpecializationSchema", only=("specialization_name",))
    )

    class Meta:
        model = Lawyer
        include_fk = True
        load_instance = True
        sqla_session = db.session
