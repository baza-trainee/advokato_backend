from calendarapi.extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitors.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("specializations_categories.id"))
    lawyer_id = db.Column(db.Integer, db.ForeignKey("lawyers.id"))
    appointment_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"Appointment: {self.visitor_id}. Question: {self.question_id}"
