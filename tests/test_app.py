
import pytest
from app import app, init_db, get_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    database = str(tmp_path / "test.db")
    monkeypatch.setattr("app.DB_PATH", database)

    app.config["TESTING"] = True

    with app.app_context():
        init_db()

    with app.test_client() as client:
        yield client


def count_submissions():
    with get_db() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM submissions"
        ).fetchone()[0]


def test_valid_submission(client):
    response = client.post("/", data={
        "name": "Ali Ahmed",
        "reg_no": "FA23-BAI-001",
        "title": "DevOps Assignment",
        "url": "https://github.com/example/project"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Assignment submitted successfully" in response.data
    assert b"Ali Ahmed" in response.data
    assert count_submissions() == 1


def test_missing_registration(client):
    response = client.post("/", data={
        "name": "Ali Ahmed",
        "reg_no": "",
        "title": "DevOps Assignment",
        "url": "https://github.com/example/project"
    })

    assert b"All fields are required" in response.data
    assert count_submissions() == 0


def test_invalid_url(client):
    response = client.post("/", data={
        "name": "Ali Ahmed",
        "reg_no": "FA23-BAI-001",
        "title": "DevOps Assignment",
        "url": "invalid-url"
    })

    assert b"Invalid submission URL" in response.data
    assert count_submissions() == 0
