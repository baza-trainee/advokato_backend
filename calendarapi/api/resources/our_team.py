from typing import List

from flask_restful import Resource

from calendarapi.api.schemas import OurTeamSchema, AboutCompanySchema
from calendarapi.extensions import db
from calendarapi.models import OurTeam, AboutCompany


class OurTeamResource(Resource):
    """
    Our Team Resource

    ---
    get:
      tags:
        - Website content
      summary: Get information about the company and its team.
      description: Get information about the company and its team.
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
                      title:
                        type: string
                      photo_path:
                        type: string
                      description:
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
                        photo_path:
                          type: string
                        description:
                          type: string
        404:
          description: No information found.
    """
    our_team_schema: OurTeamSchema = OurTeamSchema()
    company_schema: AboutCompanySchema = AboutCompanySchema()

    def get(self):
        company: AboutCompany = db.session.query(AboutCompany).first()
        team: List[OurTeam] = db.session.query(OurTeam).all()
        return {
            "company": self.company_schema.dump(company, many=False),
            "team": self.our_team_schema.dump(team, many=True),
        }, 200
