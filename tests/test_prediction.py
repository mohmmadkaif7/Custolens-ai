from src.prediction_pipeline import (
    predict_customer_segment,
    predict_customer_details
)


VALID_SEGMENTS = ["Premium", "Regular", "Budget"]


def test_customer_prediction():
    result = predict_customer_segment(
        age=30,
        income=600000,
        purchase_frequency=8,
        annual_spending=100000
    )

    assert result in VALID_SEGMENTS


def test_prediction_details():
    result = predict_customer_details(
        age=30,
        income=600000,
        purchase_frequency=8,
        annual_spending=100000
    )

    assert result is not None

    assert "confidence" in result
    assert "probabilities" in result
    assert "recommendations" in result


def test_prediction_confidence():
    result = predict_customer_details(
        age=30,
        income=600000,
        purchase_frequency=8,
        annual_spending=100000
    )

    confidence = result["confidence"]

    assert isinstance(confidence, (int, float))
    assert 0 <= confidence <= 1


def test_prediction_probabilities():
    result = predict_customer_details(
        age=30,
        income=600000,
        purchase_frequency=8,
        annual_spending=100000
    )

    probabilities = result["probabilities"]

    assert isinstance(probabilities, dict)

    assert set(probabilities.keys()) == set(VALID_SEGMENTS)

    for probability in probabilities.values():
        assert 0 <= probability <= 1

    assert abs(sum(probabilities.values()) - 1) < 0.001


def test_prediction_segment_is_valid():
    result = predict_customer_details(
        age=45,
        income=1000000,
        purchase_frequency=12,
        annual_spending=200000
    )

    probabilities = result["probabilities"]

    predicted_segment = max(
        probabilities,
        key=probabilities.get
    )

    assert predicted_segment in VALID_SEGMENTS


def test_prediction_recommendations():
    result = predict_customer_details(
        age=30,
        income=600000,
        purchase_frequency=8,
        annual_spending=100000
    )

    recommendations = result["recommendations"]

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0