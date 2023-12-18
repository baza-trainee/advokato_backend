from calendarapi.models import News
from calendarapi.extensions import fm, ma, db


class NewsSchema(fm.SQLAlchemyAutoSchema):
    name = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=4, max=100)
    )
    photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    description = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=1000)
    )

    class Meta:
        model = News
        include_fk = True
        load_instance = True
        sqla_session = db.session
