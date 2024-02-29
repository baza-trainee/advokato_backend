from typing import List
from flask import current_app

from flask_restful import Resource, request

from calendarapi.config import DAY
from calendarapi.api.schemas import OurTeamSchema, AboutCompanySchema
from calendarapi.models import OurTeam, AboutCompany
from calendarapi.extensions import (
    db,
    cache,
)


class OurTeamResource(Resource):
    our_team_schema: OurTeamSchema = OurTeamSchema()
    company_schema: AboutCompanySchema = AboutCompanySchema()

    @cache.cached(
        key_prefix=lambda: f"team_list_{request.args.get('is_slider', 'false').lower()}",
        timeout=DAY,
    )
    def get(self):
        is_slider = request.args.get("is_slider", "false").lower() == "true"
        company: AboutCompany = db.session.query(
            AboutCompany.our_team_page_description,
            AboutCompany.our_team_page_photo_path,
        ).first()
        team: List[OurTeam] = db.session.query(OurTeam).order_by("id").all()

        if is_slider:
            first_slide = db.session.query(AboutCompany).first()
            team = [
                {
                    "id": member.id,
                    "name": member.name,
                    "position": member.position,
                    "slider_photo_path": f"{current_app.config.get('BASE_URL')}/{member.slider_photo_path}",
                }
                for member in team
                if member.slider_photo_path
            ]
            schema = [
                {
                    "name": "",
                    "position": "",
                    "slider_photo_path": f"{current_app.config.get('BASE_URL')}/{first_slide.first_slider_photo_path}",
                    "id": 0,
                }
            ]
            schema += self.our_team_schema.dump(team, many=True)
            return schema

        company_data = self.company_schema.dump(company)
        return {
            "company": {
                "our_team_page_description": company_data["our_team_page_description"],
                "our_team_page_photo_path": f"{current_app.config.get('BASE_URL')}/{company_data['our_team_page_photo_path']}",
            },
            "team": self.our_team_schema.dump(team, many=True),
        }, 200
