from typing import List

from flask_restful import Resource
from sqlalchemy import desc

# from calendarapi.config import DAY
from calendarapi.api.schemas import NewsSchema
from calendarapi.extensions import (
    db,
    # cache,
)
from calendarapi.models import News


class NewsResource(Resource):
    """
    News Resource

    ---
    get:
      tags:
        - Website content
      summary: Get a list of news.
      description: Get a list of news.
      responses:
        200:
          description: List of news
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
                    created_at:
                        type: string
        404:
          description: No news found.
    """

    news_schema: NewsSchema = NewsSchema()

    # @cache.cached(key_prefix="news_list", timeout=DAY)
    def get(self):
        news: List[News] = db.session.query(News).order_by(desc(News.created_at)).all()
        return self.news_schema.dump(news, many=True), 200
