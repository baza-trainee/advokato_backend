from calendarapi.extensions import db


class Specialization(db.Model):
    __tablename__ = "specializations"

    id = db.Column(db.Integer, primary_key=True)
    specialization_name = db.Column(db.String(255), nullable=False, unique=True)
    specialization_photo = db.Column(db.String(300))
    specialization_description = db.Column(db.String(1000))
    specialization_description_full = db.Column(db.String(3000))

    def __repr__(self):
        return f"{self.specialization_name}"
