from calendarapi.extensions import db

# from calendarapi.services.cache_invalidator import invalidate_cache


class Possibilities(db.Model):
    __tablename__ = "possibilities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    short_text = db.Column(db.String(300), nullable=False)
    photo_path = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=False)


# invalidate_cache(Possibilities, "possibilities")
