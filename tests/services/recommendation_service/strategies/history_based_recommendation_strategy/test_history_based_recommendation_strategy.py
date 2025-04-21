from services.recommendation_service.strategies.history_strategy import (
    HistoryBasedRecommendationStrategy,
)
from models.recommendation import Recommendation


class TestHistoryBasedRecommendationStrategy:
    def test_if_should_return_at_least_one_recommendation(self):
        # Arrange
        strategy = HistoryBasedRecommendationStrategy()

        # Act
        recommendations = strategy.recommend("u1001")

        # Assert
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert isinstance(recommendations[0], Recommendation)  # noqa

    def test_if_recommendation_should_have_score_from_purchase(self):
        # Arrange
        strategy = HistoryBasedRecommendationStrategy()

        # Act
        recommendations = strategy.recommend("u1001")
        purchase_recs = [
            r for r in recommendations if "comprado anteriormente" in r.reason
        ]

        # Assert
        assert len(purchase_recs) > 0
        assert all(r.score >= 0.4 for r in purchase_recs)

    def test_if_recommendation_should_have_score_from_cart(self):
        # Arrange
        strategy = HistoryBasedRecommendationStrategy()

        # Act
        recommendations = strategy.recommend("u1001")
        cart_recs = [
            r for r in recommendations if "adicionado ao carrinho" in r.reason
        ]

        # Assert
        assert len(cart_recs) > 0
        assert all(r.score >= 0.3 for r in cart_recs)

    def test_if_recommendation_should_have_score_from_browsing(self):
        # Arrange
        strategy = HistoryBasedRecommendationStrategy()

        # Act
        recommendations = strategy.recommend("u1001")
        browsed_recs = [
            r for r in recommendations if "visitado recentemente" in r.reason
        ]

        # Assert
        assert len(browsed_recs) > 0
        assert all(r.score >= 0.2 for r in browsed_recs)

    def test_if_recommendation_should_have_score_from_preferences(self):
        # Arrange
        strategy = HistoryBasedRecommendationStrategy()

        # Act
        recommendations = strategy.recommend("u1001")
        preference_recs = [
            r for r in recommendations if "alinha com preferências" in r.reason
        ]

        # Assert
        assert len(preference_recs) > 0
        assert all(r.score >= 0.1 for r in preference_recs)

    def test_if_maximum_score_should_be_capped_at_1(self):
        # Arrange
        strategy = HistoryBasedRecommendationStrategy()

        # Act
        recommendations = strategy.recommend("u1001")
        top_scores = [r.score for r in recommendations if r.score >= 1.0]

        # Assert
        assert all(score <= 1.0 for score in top_scores)
