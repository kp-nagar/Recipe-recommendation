from app import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_index_url():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Recipe recommendation service is up."
