from calendarapi.extensions import db

from calendarapi.services.cache_invalidator import invalidate_cache


class HeroBlock(db.Model):
    __tablename__ = "hero_block"

    id = db.Column(db.Integer, primary_key=True)
    slogan = db.Column(db.String(30), nullable=False)
    left_text = db.Column(db.String(200), nullable=False)
    right_text = db.Column(db.String(200), nullable=False)


invalidate_cache(HeroBlock, "hero_block")
