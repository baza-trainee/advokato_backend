from calendarapi.extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitors.id"))
    specialization = db.Column(db.String, nullable=False)
    lawyer = db.Column(db.String, nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"visitor_id: {self.visitor_id}. Question: {self.specialization}"
