from datetime import datetime

from calendarapi.extensions import db

from calendarapi.services.cache_invalidator import invalidate_cache


class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2000), nullable=False, unique=True)
    specialization_name = db.Column(db.String(255), nullable=False)
    photo_path = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


invalidate_cache(News, "news_list")
