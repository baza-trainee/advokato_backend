from calendarapi.extensions import db


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(500))

    def __repr__(self):
        return f"{self.city_name}"
