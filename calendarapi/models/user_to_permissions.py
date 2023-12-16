from calendarapi.extensions import db


class UsersToPermissions(db.Model):
    __tablename__ = "users_to_permissions"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    )
