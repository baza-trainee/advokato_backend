from calendarapi.models import OurTeam
from calendarapi.extensions import fm, ma, db


class OurTeamSchema(fm.SQLAlchemyAutoSchema):
    name = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=4, max=100)
    )
    photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    description = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=500)
    )

    class Meta:
        model = OurTeam
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
