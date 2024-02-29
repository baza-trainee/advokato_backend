from calendarapi.extensions import db

from calendarapi.services.cache_invalidator import invalidate_cache


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f"{self.city_name}"


invalidate_cache(City, "contact_list")
