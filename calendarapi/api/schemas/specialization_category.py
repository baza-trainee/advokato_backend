from flask import current_app
from marshmallow import pre_dump
from calendarapi.models import Specialization
from calendarapi.extensions import fm, db, ma


class SpecializationSchema(fm.SQLAlchemyAutoSchema):
    specialization_name = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=100)
    )
    specialization_photo = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    specialization_description = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=10, max=1000)
    )
    specialization_description_full = ma.fields.String(
        validate=ma.fields.validate.Length(max=3000)
    )

    @pre_dump
    def add_base_url(self, data, **kwargs):
        field_name = "specialization_photo"
        field_data = getattr(data, field_name, None)
        if field_data:
            setattr(
                data, field_name, f"{current_app.config.get('BASE_URL')}/{field_data}"
            )
        return data

    class Meta:
        model = Specialization
        include_fk = True
        load_instance = True
        sqla_session = db.session
