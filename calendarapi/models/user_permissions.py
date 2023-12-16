from calendarapi.extensions import db


class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    view_name = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return self.view_name
