from flask import current_app
from marshmallow import pre_load, pre_dump

from calendarapi.models import OurTeam
from calendarapi.extensions import fm, ma, db


class OurTeamSchema(fm.SQLAlchemyAutoSchema):
    name = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=4, max=100)
    )
    position = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=4, max=100)
    )
    photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    slider_photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    description = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=500)
    )

    @pre_dump
    def add_base_url(self, data, **kwargs):
        for field_name in ["photo_path", "slider_photo_path"]:
            field_data = getattr(data, field_name, None)
            if field_data:
                setattr(
                    data,
                    field_name,
                    f"{current_app.config.get('BASE_URL')}/{field_data}",
                )
        return data

    class Meta:
        model = OurTeam
        include_fk = True
        load_instance = True
        sqla_session = db.session
