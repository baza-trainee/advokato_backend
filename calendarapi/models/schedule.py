from calendarapi.extensions import db


class Schedule(db.Model):
    __tablename__ = "schedules"

    id = db.Column(db.Integer, primary_key=True)
    lawyer_id = db.Column(
        db.Integer,
        db.ForeignKey("lawyers.id"),
    )
    date = db.Column(db.Date)
    time = db.Column(db.ARRAY(db.Time))
