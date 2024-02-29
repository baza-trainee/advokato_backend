from calendarapi.extensions import db


class layersToSchedule(db.Model):
    __tablename__ = "layers_to_schedules"

    lawyer_id = db.Column(db.Integer, db.ForeignKey("lawyers.id"), primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), primary_key=True)
