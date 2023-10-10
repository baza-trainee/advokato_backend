from typing import Dict

from flask.testing import FlaskClient


def test_revoke_access_token(client: FlaskClient, admin_headers: Dict[str, str]):
    resp = client.delete("/auth/revoke_access", headers=admin_headers)
    assert resp.status_code == 200

    resp = client.get("/api/v1/users", headers=admin_headers)
    assert resp.status_code == 401


def test_revoke_refresh_token(
    client: FlaskClient, admin_refresh_headers: Dict[str, str]
):
    resp = client.delete("/auth/revoke_refresh", headers=admin_refresh_headers)
    assert resp.status_code == 200

    resp = client.post("/auth/refresh", headers=admin_refresh_headers)
    assert resp.status_code == 401
