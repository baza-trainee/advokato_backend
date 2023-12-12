from calendarapi.models import Client
from calendarapi.extensions import fm, ma, db


class ClientSchema(fm.SQLAlchemyAutoSchema):
    
    photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )

    class Meta:
        model = Client
        exclude = ["id"]
        load_instance = True
        sqla_session = db.session
