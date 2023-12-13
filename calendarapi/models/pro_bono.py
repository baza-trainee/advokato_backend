from calendarapi.extensions import db


class ProBono(db.Model):
    __tablename__ = "pro_bono"

    id = db.Column(db.Integer, primary_key=True)
    photo_path = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(3000), nullable=False, unique=True)
