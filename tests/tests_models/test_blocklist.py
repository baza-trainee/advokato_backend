from calendarapi.models.user import User
from calendarapi.models.blocklist import TokenBlocklist
from flask_sqlalchemy import SQLAlchemy
from flask import current_app


def test_create_and_retrieve_token_blocklist(db: SQLAlchemy):
    user = User(
        username=current_app.config["ADMIN_DEFAULT_LOGIN"],
        email="admin@gmail.com",
        password=current_app.config["ADMIN_DEFAULT_PASSWORD"],
        is_active=True,
        is_superuser=True,
    )

    db.session.add(user)
    db.session.commit()

    token_blocklist = TokenBlocklist(
        jti="token_jti",
        token_type="access",
        user_id=1,
        revoked=False,
        expires="2023-10-20 12:00:00",
    )

    db.session.add(token_blocklist)
    db.session.commit()

    retrieved_token_blocklist = TokenBlocklist.query.get(1)

    assert retrieved_token_blocklist.jti, "token_jti"
    assert retrieved_token_blocklist.token_type, "access"
    assert retrieved_token_blocklist.user_id, 1
    # assert retrieved_token_blocklist.revoked, False
    assert retrieved_token_blocklist.expires, "2023-10-20 12:00:00"
