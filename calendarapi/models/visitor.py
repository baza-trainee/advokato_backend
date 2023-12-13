from calendarapi.extensions import db


class Visitor(db.Model):
    __tablename__ = "visitors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    is_beneficiary = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.name}"
