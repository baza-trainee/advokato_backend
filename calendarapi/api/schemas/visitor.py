from calendarapi.models import Visitor
from calendarapi.extensions import fm, db, ma

phone_number_pattern = r"^(?:\+?380|\b380|0)[0-9]{9,13}$"


class VisitorSchema(fm.SQLAlchemyAutoSchema):
    email = ma.fields.String(validate=ma.fields.validate.Email(), allow_none=True)
    name = ma.fields.String(
        validate=ma.fields.validate.Length(min=2, max=100), allow_none=True
    )
    phone_number = ma.fields.String(
        required=True,
        validate=ma.fields.validate.Regexp(
            phone_number_pattern, error="Invalid phone number format"
        ),
    )
    is_beneficiary = ma.fields.Boolean()

    class Meta:
        model = Visitor
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
