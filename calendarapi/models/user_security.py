from calendarapi.extensions import db


class UserSecurity(db.Model):
    __tablename__ = "user_security"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    token = db.Column(db.String, nullable=False)
