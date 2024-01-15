from flask import current_app
from flask_restful import Resource
from sqlalchemy import exc

from calendarapi.api.schemas import AboutCompanySchema, HeroBlockSchema
from calendarapi.models import HeroBlock, AboutCompany

from calendarapi.config import DAY
from calendarapi.extensions import (
    db,
    cache,
)


class HeroBlockResource(Resource):
    company_schema: AboutCompanySchema = AboutCompanySchema()
    hero_schema: HeroBlockSchema = HeroBlockSchema()

    @cache.cached(key_prefix="hero_block", timeout=DAY)
    def get(self):
        try:
            hero_data = db.session.query(HeroBlock).first()
            company: AboutCompany = db.session.query(
                AboutCompany.main_page_description,
                AboutCompany.main_page_photo_path,
            ).first()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database error: {str(e)}"}, 500

        company_data = self.company_schema.dump(company)
        return {
            "company": self.company_schema.dump(company, many=False),
            "company": {
                "main_page_description": company_data["main_page_description"],
                "main_page_photo_path": f"{current_app.config.get('BASE_URL')}/{company_data['main_page_photo_path']}",
            },
            "hero": self.hero_schema.dump(hero_data, many=False),
        }, 200
