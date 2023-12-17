from flask_restful import Resource
from sqlalchemy import exc

from calendarapi.api.schemas import AboutCompanySchema, HeroBlockSchema
# from calendarapi.config import DAY
from calendarapi.extensions import (
    db,
    # cache,
)
from calendarapi.models import HeroBlock, AboutCompany


class HeroBlockResource(Resource):
    """
    Hero Block Resource

    ---
    get:
      tags:
        - Website content
      summary: Get information about the hero block.
      description: Retrieve data for the hero block, including slogan, left text, and right text.
      responses:
        200:
          description: Information about the hero block.
          content:
            application/json:
              schema:
                type: object
                properties:
                  hero:
                    type: object
                    properties:
                      slogan:
                        type: string
                      left_text:
                        type: string
                      right_text:
                        type: string
                  company:
                    type: object
                    properties:
                      main_page_photo_path:
                        type: string
                      main_page_description:
                        type: string
        404:
          description: No information found.
    """

    company_schema: AboutCompanySchema = AboutCompanySchema()
    hero_schema: HeroBlockSchema = HeroBlockSchema()

    # @cache.cached(key_prefix="hero_block", timeout=DAY)
    def get(self):
        try:
            hero_data = db.session.query(HeroBlock).first()
            company: AboutCompany = db.session.query(
                AboutCompany.main_page_photo_path, AboutCompany.main_page_description
            ).first()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database error: {str(e)}"}, 500
        return {
            "company": self.company_schema.dump(company, many=False),
            "hero": self.hero_schema.dump(hero_data, many=False),
        }, 200
