from typing import List
from flask import request
from flask_restful import Resource

from calendarapi.api.schemas import OurTeamSchema, AboutCompanySchema
from calendarapi.extensions import (
    db,
    # cache,
)
from calendarapi.models import OurTeam, AboutCompany
# from calendarapi.config import DAY


class OurTeamResource(Resource):
    """
    Our Team Resource

    ---
    get:
      tags:
        - Website content
      summary: Get information about the company and its team.
      description: |
        If the `is_slider` parameter is set to `True`, the response will include only the fields: id, name, position, and slider_photo_path.

      parameters:
        - in: query
          name: is_slider
          schema:
            type: boolean
          description: Flag to determine whether to return slider data. Returns only records that have a photo for the slider.
      responses:
        200:
          description: Information about the company and its team.
          content:
            application/json:
              schema:
                type: object
                properties:
                  company:
                    type: object
                    properties:
                      our_team_page_description:
                        type: string
                      our_team_page_photo_path:
                        type: string
                  team:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
                        position:
                          type: string
                        photo_path:
                          type: string
                        slider_photo_path:
                          type: string
                        description:
                          type: string
        404:
          description: No information found.
    """

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
