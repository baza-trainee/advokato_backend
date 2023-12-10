from calendarapi.extensions import db
from calendarapi.services.cache_invalidator import invalidate_cache


class OurTeam(db.Model):
    __tablename__ = "our_team"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo_path = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(3000), nullable=False, unique=True)


invalidate_cache(OurTeam, "team_list")
