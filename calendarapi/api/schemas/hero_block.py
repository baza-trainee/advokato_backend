from calendarapi.models import HeroBlock
from calendarapi.extensions import fm, db, ma


class HeroBlockSchema(fm.SQLAlchemyAutoSchema):
    slogan = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=30)
    )
    left_text = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=200)
    )
    right_text = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=200)
    )

    class Meta:
        model = HeroBlock
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
