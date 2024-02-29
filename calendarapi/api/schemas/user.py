from calendarapi.models import User
from calendarapi.extensions import fm, db, ma
from calendarapi.commons.exeptions import INVALID_EMAIL


class UserSchema(fm.SQLAlchemyAutoSchema):
    id = ma.fields.Int(dump_only=True)
    password = ma.fields.String(load_only=True, required=True)
    email = ma.fields.String(
        required=True,
        validate=[
            ma.fields.validate.Email(error=INVALID_EMAIL),
        ],
    )

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)
