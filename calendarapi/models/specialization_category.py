from calendarapi.extensions import db


class SpecializationCategory(db.Model):
    __tablename__ = "specializations_categories"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), unique=True)
    price = db.Column(db.Integer, nullable=False)
    consultation_time_required = db.Column(db.Integer)

    def __repr__(self):
        return f"Question: {self.question}"
