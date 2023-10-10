from calendarapi.extensions import db


class SpecializationsToLawyers(db.Model):
    __tablename__ = "specializations_to_lawyers"

    question_id = db.Column(
        db.Integer, db.ForeignKey("specializations_categories.id"), primary_key=True
    )
    lawyer_id = db.Column(db.Integer, db.ForeignKey("lawyers.id"), primary_key=True)
