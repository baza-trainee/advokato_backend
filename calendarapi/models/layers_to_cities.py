from calendarapi.extensions import db


class layersToCities(db.Model):
    __tablename__ = "layers_to_cities"

    lawyer_id = db.Column(db.Integer, db.ForeignKey("lawyers.id"), primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), primary_key=True)
