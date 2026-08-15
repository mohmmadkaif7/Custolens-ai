from src.recommendation_engine import generate_recommendations


VALID_SEGMENTS = ["Premium", "Regular", "Budget"]


def test_premium_recommendations():
    result = generate_recommendations("Premium")

    assert result is not None
    assert isinstance(result, dict)

    assert "strategy" in result
    assert "recommendations" in result

    assert isinstance(result["strategy"], str)
    assert len(result["strategy"]) > 0

    assert isinstance(result["recommendations"], list)
    assert len(result["recommendations"]) > 0


def test_regular_recommendations():
    result = generate_recommendations("Regular")

    assert result is not None
    assert isinstance(result, dict)

    assert "strategy" in result
    assert "recommendations" in result

    assert isinstance(result["recommendations"], list)
    assert len(result["recommendations"]) > 0


def test_budget_recommendations():
    result = generate_recommendations("Budget")

    assert result is not None
    assert isinstance(result, dict)

    assert "strategy" in result
    assert "recommendations" in result

    assert isinstance(result["recommendations"], list)
    assert len(result["recommendations"]) > 0


def test_all_segments_have_recommendations():
    for segment in VALID_SEGMENTS:
        result = generate_recommendations(segment)

        assert isinstance(result, dict)
        assert "strategy" in result
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0


def test_recommendations_are_strings():
    for segment in VALID_SEGMENTS:
        result = generate_recommendations(segment)

        for recommendation in result["recommendations"]:
            assert isinstance(recommendation, str)
            assert len(recommendation.strip()) > 0


def test_invalid_segment_returns_general_strategy():
    result = generate_recommendations("Unknown")

    assert isinstance(result, dict)
    assert result["strategy"] == "General customer engagement"
    assert len(result["recommendations"]) > 0