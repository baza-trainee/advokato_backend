from calendarapi.extensions import db


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    photo_path = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(300), unique=True, nullable=True)
    
