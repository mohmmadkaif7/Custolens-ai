from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


VALID_SEGMENTS = ["Premium", "Regular", "Budget"]


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200


def test_predict_endpoint():
    payload = {
        "age": 30,
        "income": 600000,
        "purchase_frequency": 8,
        "annual_spending": 100000
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "predicted_segment" in data
    assert "recommendations" in data


def test_predict_endpoint_valid_segment():
    payload = {
        "age": 45,
        "income": 1000000,
        "purchase_frequency": 12,
        "annual_spending": 200000
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["predicted_segment"] in VALID_SEGMENTS


def test_predict_endpoint_recommendations():
    payload = {
        "age": 30,
        "income": 600000,
        "purchase_frequency": 8,
        "annual_spending": 100000
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    recommendations = data["recommendations"]

    assert isinstance(recommendations, dict)
    assert "strategy" in recommendations
    assert "recommendations" in recommendations

    assert isinstance(recommendations["strategy"], str)
    assert len(recommendations["strategy"]) > 0

    assert isinstance(recommendations["recommendations"], list)
    assert len(recommendations["recommendations"]) > 0


def test_predict_endpoint_invalid_data():
    payload = {
        "age": "invalid",
        "income": 600000,
        "purchase_frequency": 8,
        "annual_spending": 100000
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422