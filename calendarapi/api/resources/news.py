from typing import List

from flask_restful import Resource
from sqlalchemy import desc, exc

from calendarapi.config import DAY
from calendarapi.api.schemas import NewsSchema
from calendarapi.models import News
from calendarapi.extensions import (
    db,
    cache,
)


class NewsResource(Resource):
    news_schema: NewsSchema = NewsSchema()

    @cache.cached(key_prefix="news_list", timeout=DAY)
    def get(self):
        try:
            news: List[News] = (
                db.session.query(News).order_by(desc(News.created_at)).all()
            )
        except exc.SQLAlchemyError as e:
            return {"error": f"Database error: {str(e)}"}, 500
        return self.news_schema.dump(news, many=True), 200
