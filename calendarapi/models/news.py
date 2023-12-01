from calendarapi.extensions import db
from datetime import datetime


class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False, unique=True)    
    photo_path = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)