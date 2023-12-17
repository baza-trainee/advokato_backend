from calendarapi.extensions import db
# from calendarapi.services.cache_invalidator import invalidate_cache


class ProBono(db.Model):
    __tablename__ = "pro_bono"

    id = db.Column(db.Integer, primary_key=True)
    photo_path = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(3000), nullable=False, unique=True)


# invalidate_cache(ProBono, "pro_bono")
