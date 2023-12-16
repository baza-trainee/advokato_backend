from calendarapi.extensions import db


class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_type = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(500))

    def __repr__(self):
        return f"{self.contact_type}: {self.value}"
