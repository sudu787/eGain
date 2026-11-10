from fastapi.testclient import TestClient

from app import main


def make_client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "gridguide.sqlite3")
    return TestClient(main.app)


def test_health_and_demo_data_are_labeled(tmp_path, monkeypatch):
    with make_client(tmp_path, monkeypatch) as client:
        assert client.get("/healthz").json()["status"] == "ok"
        response = client.get("/api/v1/demo/outages")
    assert "not live utility status" in response.json()["data_type"]
    assert response.json()["outages"]


def test_report_is_persisted_and_has_demo_disclosure(tmp_path, monkeypatch):
    with make_client(tmp_path, monkeypatch) as client:
        created = client.post(
            "/api/v1/outage-reports",
            json={"service_area": "North Ridge", "issue_type": "no_power"},
        )
        assert created.status_code == 201
        receipt = created.json()
        assert receipt["reference"].startswith("GG-")
        assert "not sent to a utility" in receipt["demo_notice"]
        read_back = client.get(f"/api/v1/outage-reports/{receipt['reference']}")
    assert read_back.status_code == 200
    assert read_back.json()["reference"] == receipt["reference"]


def test_idempotency_returns_one_receipt_and_rejects_key_reuse(tmp_path, monkeypatch):
    with make_client(tmp_path, monkeypatch) as client:
        headers = {"Idempotency-Key": "scenario-123456"}
        payload = {"service_area": "Cedar Park", "issue_type": "partial_power"}
        first = client.post("/api/v1/outage-reports", json=payload, headers=headers)
        retry = client.post("/api/v1/outage-reports", json=payload, headers=headers)
        conflict = client.post(
            "/api/v1/outage-reports",
            json={"service_area": "Cedar Park", "issue_type": "no_power"},
            headers=headers,
        )
    assert first.status_code == retry.status_code == 201
    assert first.json()["reference"] == retry.json()["reference"]
    assert conflict.status_code == 409


def test_invalid_area_and_extra_personal_fields_are_rejected(tmp_path, monkeypatch):
    with make_client(tmp_path, monkeypatch) as client:
        unknown_area = client.post(
            "/api/v1/outage-reports",
            json={"service_area": "Unknown Place", "issue_type": "no_power"},
        )
        personal_data = client.post(
            "/api/v1/outage-reports",
            json={
                "service_area": "Old Town",
                "issue_type": "no_power",
                "account_number": "123456789",
            },
        )
        invalid_issue = client.post(
            "/api/v1/outage-reports",
            json={"service_area": "Old Town", "issue_type": "unsafe"},
        )
    assert unknown_area.status_code == 422
    assert personal_data.status_code == 422
    assert invalid_issue.status_code == 422


def test_bearer_auth_rejects_missing_and_wrong_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "API_KEY", "local-test-secret")
    with make_client(tmp_path, monkeypatch) as client:
        payload = {"service_area": "North Ridge", "issue_type": "no_power"}
        missing = client.post("/api/v1/outage-reports", json=payload)
        wrong = client.post(
            "/api/v1/outage-reports",
            json=payload,
            headers={"Authorization": "Bearer incorrect-secret"},
        )
        authorized = client.post(
            "/api/v1/outage-reports",
            json=payload,
            headers={"Authorization": "Bearer local-test-secret"},
        )
    assert missing.status_code == 401
    assert wrong.status_code == 401
    assert authorized.status_code == 201


def test_storage_failure_returns_recoverable_503(tmp_path, monkeypatch):
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("block", encoding="utf-8")
    normal_db = tmp_path / "working.sqlite3"
    monkeypatch.setattr(main, "DB_PATH", normal_db)
    with TestClient(main.app) as client:
        monkeypatch.setattr(main, "DB_PATH", blocker / "reports.sqlite3")
        response = client.post(
            "/api/v1/outage-reports",
            json={"service_area": "Riverbend", "issue_type": "no_power"},
        )
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "report_store_unavailable"
