from calendarapi.models import ProBono
from calendarapi.extensions import fm, ma, db


class ProBonoSchema(fm.SQLAlchemyAutoSchema):
    photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    description = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=3000)
    )

    class Meta:
        model = ProBono
        load_instance = True
        sqla_session = db.session
