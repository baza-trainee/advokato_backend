from calendarapi.extensions import db


class AboutCompany(db.Model):
    __tablename__ = "about_company"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    photo_path = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(3000), nullable=False)
