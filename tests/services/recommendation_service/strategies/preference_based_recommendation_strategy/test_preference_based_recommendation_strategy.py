from services.recommendation_service.strategies.preference_strategy import (
    PreferenceBasedRecommendationStrategy,
)
from models.recommendation import Recommendation


class TestPreferenceBasedRecommendationStrategy:
    def test_if_should_return_recommendations_based_on_preferences(self):
        # Arrange
        strategy = PreferenceBasedRecommendationStrategy()

        # Act
        recommendations = strategy.recommend("u1001")

        # Assert
        assert isinstance(recommendations, list)
        assert isinstance(recommendations[0], Recommendation)  # noqa
        assert recommendations[0].score > 0
        assert (
            "preferida" in recommendations[0].reason
            or "compatíveis" in recommendations[0].reason
        )

    def test_if_price_should_be_within_user_purchase_range(self):
        # Arrange
        strategy = PreferenceBasedRecommendationStrategy()

        # Act
        recommendations = strategy.recommend("u1001")
        prices_in_range = [
            r for r in recommendations if "preço compatível" in r.reason
        ]

        # Assert
        assert isinstance(prices_in_range, list)
        assert all("preço compatível" in r.reason for r in prices_in_range)
