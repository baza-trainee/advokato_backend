from calendarapi.models import AboutCompany
from calendarapi.extensions import fm, ma, db


class AboutCompanySchema(fm.SQLAlchemyAutoSchema):
    main_page_photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    main_page_description = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=500)
    )
    our_team_page_photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    first_slider_photo_path = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=300)
    )
    our_team_page_description = ma.fields.String(
        required=True, validate=ma.fields.validate.Length(min=2, max=3000)
    )

    class Meta:
        model = AboutCompany
        include_fk = True
        load_instance = True
        sqla_session = db.session
