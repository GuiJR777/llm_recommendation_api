from services.recommendation_service.recommendation_service import (
    RecommendationService,
)
from models.recommendation import Recommendation


class TestRecommendationService:
    def test_if_default_strategy_should_be_history(self):
        # Arrange
        service = RecommendationService()

        # Act
        recommendations = service.recommend_for_user("u1001")

        # Assert
        assert isinstance(recommendations, list)
        assert isinstance(recommendations[0], Recommendation)  # noqa
        assert recommendations[0].score > 0

    def test_if_should_switch_to_preference_strategy(self):
        # Arrange
        service = RecommendationService()

        # Act
        recommendations = service.recommend_for_user(
            "u1001", strategy_name="preference"
        )

        # Assert
        assert isinstance(recommendations, list)
        assert isinstance(recommendations[0], Recommendation)  # noqa
        assert recommendations[0].score > 0

    def test_if_invalid_strategy_should_fallback_to_history(self):
        # Arrange
        service = RecommendationService()

        # Act
        recommendations = service.recommend_for_user(
            "u1001", strategy_name="invalid"
        )

        # Assert
        assert isinstance(recommendations, list)
        assert isinstance(recommendations[0], Recommendation)  # noqa
        assert recommendations[0].score > 0
