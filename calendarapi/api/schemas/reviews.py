from calendarapi.models import Reviews
from calendarapi.extensions import fm, ma, db


class ReviewsSchema(fm.SQLAlchemyAutoSchema):
    name = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=4, max=100)
    )
    position = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=100)
    )
    photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    description = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=1000)
    )

    class Meta:
        model = Reviews
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session