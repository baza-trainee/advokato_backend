from calendarapi.models import City
from calendarapi.extensions import fm, db


class CitySchema(fm.SQLAlchemyAutoSchema):
    class Meta:
        model = City
        exclude = ["id"]
        include_fk = True
        load_instance = True
        sqla_session = db.session
