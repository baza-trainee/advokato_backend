from calendarapi.extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    visitor = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String, nullable=False)
    lawyer = db.Column(db.String, nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"Appointment: {self.visitor}. Question: {self.specialization}"
