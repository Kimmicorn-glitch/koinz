from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import engine
from app.main import app


def test_mfa_setup_and_verify() -> None:
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        login = client.post("/auth/login", json={"email": "worker@localhands.com", "password": "ChangeMe123!"})
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        setup = client.post("/auth/mfa/setup", headers=headers)
        assert setup.status_code == 200
        secret = setup.json()["secret"]
        assert len(secret) > 0

        bad = client.post("/auth/mfa/verify", headers=headers, json={"code": "000000"})
        assert bad.status_code == 200
        assert bad.json()["verified"] is False


def test_sessions_revoke() -> None:
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        login = client.post("/auth/login", json={"email": "worker@localhands.com", "password": "ChangeMe123!"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        sessions = client.get("/auth/sessions/", headers=headers)
        assert sessions.status_code == 200
        assert isinstance(sessions.json(), list)

        revoke_all = client.post("/auth/sessions/revoke-all", headers=headers)
        assert revoke_all.status_code == 200
        assert revoke_all.json()["revoked_count"] >= 0


def test_consent_grant_and_withdraw() -> None:
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        login = client.post("/auth/login", json={"email": "worker@localhands.com", "password": "ChangeMe123!"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        grant = client.post("/auth/consent/", headers=headers, json={"consent_type": "data_processing"})
        assert grant.status_code == 200
        assert grant.json()["granted"] is True

        check = client.get("/auth/consent/check", headers=headers, params={"consent_type": "data_processing"})
        assert check.status_code == 200
        assert check.json()["granted"] is True

        withdraw = client.post("/auth/consent/withdraw", headers=headers, json={"consent_type": "data_processing"})
        assert withdraw.status_code == 200
        assert withdraw.json()["granted"] is False


def test_unauthorized_access_forbidden() -> None:
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        login = client.post("/auth/login", json={"email": "worker@localhands.com", "password": "ChangeMe123!"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/auth/audit/", headers=headers)
        assert response.status_code == 403
