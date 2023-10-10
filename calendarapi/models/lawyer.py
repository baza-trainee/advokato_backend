from calendarapi.extensions import db


class Lawyer(db.Model):
    __tablename__ = "lawyers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    lawyer_mail = db.Column(db.String(100), unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))

    specializations = db.relationship(
        "SpecializationCategory",
        secondary="specializations_to_lawyers",
        backref=db.backref("lawyers", lazy=True),
    )

    def __repr__(self):
        return f"Lawyer: {self.name} {self.surname}"
