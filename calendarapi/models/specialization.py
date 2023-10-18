from calendarapi.extensions import db


class Specialization(db.Model):
    __tablename__ = "specializations"

    id = db.Column(db.Integer, primary_key=True)
    specialization_name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"{self.specialization_name}"
