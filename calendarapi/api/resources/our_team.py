from typing import List

from flask_restful import Resource, request

# from calendarapi.config import DAY
from calendarapi.api.schemas import OurTeamSchema, AboutCompanySchema
from calendarapi.models import OurTeam, AboutCompany
from calendarapi.extensions import (
    db,
    # cache,
)


class OurTeamResource(Resource):
    our_team_schema: OurTeamSchema = OurTeamSchema()
    company_schema: AboutCompanySchema = AboutCompanySchema()

    # @cache.cached(
    #     key_prefix=lambda: f"team_list_{request.args.get('is_slider', 'false').lower()}",
    #     timeout=DAY,
    # )
    def get(self):
        is_slider = request.args.get("is_slider", "false").lower() == "true"
        company: AboutCompany = db.session.query(
            AboutCompany.our_team_page_description,
            AboutCompany.our_team_page_photo_path,
        ).first()
        team: List[OurTeam] = db.session.query(OurTeam).all()
        if is_slider:
            team = [
                {
                    "id": member.id,
                    "name": member.name,
                    "position": member.position,
                    "slider_photo_path": member.slider_photo_path,
                }
                for member in team
                if member.slider_photo_path
            ]
            return self.our_team_schema.dump(team, many=True)
        return {
            "company": self.company_schema.dump(company, many=False),
            "team": self.our_team_schema.dump(team, many=True),
        }, 200
