from typing import List

from flask_restful import Resource
from sqlalchemy import desc
# from flask_jwt_extended import jwt_required

from calendarapi.api.schemas import ReviewsSchema
from calendarapi.extensions import db
from calendarapi.models import Reviews


class ReviewsResource(Resource):
    """
    Reviews Resource

    ---
    get:
      tags:
        - Website content
      summary: Get a list of reviews.
      description: Get a list of reviews.
      responses:
        200:
          description: List of reviews
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
                    description:
                      type: string
                    photo_path:
                      type: string
        404:
          description: No reviews found.
    """

    # method_decorators = [jwt_required()]
    reviews_schema: ReviewsSchema = ReviewsSchema()

    def get(self):
        reviews: List[Reviews] = db.session.query(Reviews).order_by(desc(Reviews.id)).all()
        return self.reviews_schema.dump(reviews, many=True), 200