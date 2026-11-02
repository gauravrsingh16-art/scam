"""
Automated Unit Tests for FastAPI Serverless Endpoints
Tests health, single prediction, email analysis, bulk prediction, metrics, history, and settings.
"""

import io
import pytest
from fastapi.testclient import TestClient
from api.index import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["version"] == "2.0.0"


def test_dashboard_stats_endpoint(client):
    response = client.get("/api/dashboard-stats")
    assert response.status_code == 200
    data = response.json()
    assert "kpi" in data
    assert "distribution" in data
    assert "total_processed" in data["kpi"]


def test_predict_spam(client):
    payload = {
        "text": "URGENT: You have won £1,000 cash prize! Claim immediately at http://claim.xyz",
        "message_type": "SMS",
        "log_to_db": False
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["is_spam"] is True
    assert data["data"]["label"] == "SPAM"
    assert data["data"]["confidence"] >= 0.5


def test_predict_ham(client):
    payload = {
        "text": "Hey are we still meeting for lunch tomorrow at 1pm?",
        "message_type": "SMS",
        "log_to_db": False
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["is_spam"] is False
    assert data["data"]["label"] == "NOT SPAM"
    assert data["data"]["confidence"] >= 0.5


def test_predict_empty_validation(client):
    response = client.post("/api/predict", json={"text": "   "})
    assert response.status_code == 400


def test_email_analysis_endpoint(client):
    payload = {
        "subject": "Urgent: Verify Your Account Credentials",
        "sender": "security-alert@paypal.suspicious-domain.xyz",
        "body": "Dear customer, your bank account is suspended. Verify credentials immediately.",
        "log_to_db": False
    }
    response = client.post("/api/email-analysis", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "heuristics" in data["data"]
    assert data["data"]["heuristics"]["has_indicators"] is True


def test_bulk_predict_endpoint(client):
    csv_content = 'text\n"WINNER!! You have won a 1000 prize"\n"Hey buddy, see you at the office"\n'
    file_bytes = io.BytesIO(csv_content.encode("utf-8"))
    response = client.post(
        "/api/bulk-predict",
        files={"file": ("test.csv", file_bytes, "text/csv")},
        data={"log_to_db": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["summary"]["total"] == 2
    assert len(data["rows"]) == 2


def test_model_metrics_endpoint(client):
    response = client.get("/api/model-metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "metrics" in data
    assert "test_metrics" in data["metrics"]
    assert "accuracy" in data["metrics"]["test_metrics"]


def test_history_and_settings_endpoints(client):
    # Query history
    r_hist = client.get("/api/history?limit=5")
    assert r_hist.status_code == 200
    assert "records" in r_hist.json()

    # Get settings
    r_sett = client.get("/api/settings")
    assert r_sett.status_code == 200
    assert "history_enabled" in r_sett.json()
