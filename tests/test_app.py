import pytest
from app import app, db, MyTask

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Task Smash" in response.data  # check for expected text

def test_add_task(client):
    response = client.post("/", data={"content": "Test Task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Task" in response.data

    # Check if task is actually in the database
    task = MyTask.query.filter_by(content="Test Task").first()
    assert task is not None
