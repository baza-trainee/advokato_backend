from typing import List

from flask_restful import Resource
from sqlalchemy import desc, exc

from calendarapi.config import DAY
from calendarapi.api.schemas import ReviewsSchema
from calendarapi.models import Reviews
from calendarapi.extensions import (
    db,
    cache,
)


class ReviewsResource(Resource):
    reviews_schema: ReviewsSchema = ReviewsSchema()

    @cache.cached(key_prefix="reviews_list", timeout=DAY)
    def get(self):
        try:
            reviews: List[Reviews] = (
                db.session.query(Reviews).order_by(desc(Reviews.id)).all()
            )
        except exc.SQLAlchemyError as e:
            return {"error": f"Database error: {str(e)}"}, 500
        return self.reviews_schema.dump(reviews, many=True), 200
