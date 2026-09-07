from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import engine
from app.main import app


def test_ingestion_requires_admin() -> None:
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        login = client.post("/auth/login", json={"email": "worker@localhands.com", "password": "ChangeMe123!"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post("/ingestion/accounts", headers=headers, json={
            "external_id": "acct-1",
            "source": "bank-a",
            "account_type": "checking",
            "currency": "zar",
            "holder_name": "Nomsa D",
        })
        assert response.status_code == 403


def test_enrichment_currency_normalization() -> None:
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        response = client.post("/enrichment/enrich", json={
            "amount": 100.0,
            "currency": "zar",
            "holder_name": "Nomsa Dlamini",
            "bank_name": "FNB",
        })
        assert response.status_code == 200
        body = response.json()
        assert body["normalized"] is True
        assert body["threat_level"] == "none"
