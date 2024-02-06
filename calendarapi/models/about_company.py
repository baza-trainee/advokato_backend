from calendarapi.extensions import db

from calendarapi.services.cache_invalidator import invalidate_cache


class AboutCompany(db.Model):
    __tablename__ = "about_company"

    id = db.Column(db.Integer, primary_key=True)
    main_page_photo_path = db.Column(db.String(300), nullable=False)
    our_team_page_photo_path = db.Column(db.String(300), nullable=False)
    first_slider_photo_path = db.Column(db.String(300))
    main_page_description = db.Column(db.String(500), nullable=False)
    our_team_page_description = db.Column(db.String(3000), nullable=False)


invalidate_cache(AboutCompany, "hero_block")
invalidate_cache(AboutCompany, "team_list_false")
invalidate_cache(AboutCompany, "team_list_true")
