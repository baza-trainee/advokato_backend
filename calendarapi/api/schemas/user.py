from calendarapi.models import User
from calendarapi.extensions import fm, db, ma


class UserSchema(fm.SQLAlchemyAutoSchema):
    id = ma.fields.Int(dump_only=True)
    password = ma.fields.String(load_only=True, required=True)
    email = ma.fields.String(
        required=True,
        validate=[
            ma.fields.validate.Email(error="Невірний формат пошти."),
        ],
    )

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = (
            "_password",
            "is_superuser",
        )
