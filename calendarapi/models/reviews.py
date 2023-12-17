from datetime import date

from calendarapi.extensions import db

# from calendarapi.services.cache_invalidator import invalidate_cache


class Reviews(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(1000), nullable=False, unique=True)
    photo_path = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.Date, default=date.today())


# invalidate_cache(Reviews, "reviews_list")
