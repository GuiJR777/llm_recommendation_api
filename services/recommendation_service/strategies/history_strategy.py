from services.recommendation_service.strategies.base_strategy import (
    RecommendationStrategy,
)
from models.recommendation import Recommendation
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository


class HistoryBasedRecommendationStrategy(RecommendationStrategy):
    def __init__(self):
        self.user_repo = UserRepository()
        self.product_repo = ProductRepository()

    def recommend(self, user_id: str) -> list[Recommendation]:
        user = self.user_repo.get_by_id(user_id)
        purchased_ids = [p["product_id"] for p in user.purchase_history]
        cart_ids = [
            e["product_id"] for e in user.cart_events if e["action"] == "add"
        ]
        browsed_ids = [b["product_id"] for b in user.browsing_history]
        preferences = user.preferences

        recommendations = []

        for product_data in self.product_repo.products:
            product_id = product_data["product_id"]
            score = 0.0
            reason_parts = []

            if product_id in purchased_ids:
                score += 0.4
                reason_parts.append("comprado anteriormente")

            if product_id in cart_ids:
                score += 0.3
                reason_parts.append("adicionado ao carrinho")

            if product_id in browsed_ids:
                score += 0.2
                reason_parts.append("visitado recentemente")

            # Preferência (menor peso, extra boost)
            if (
                product_data["category"] in preferences.get("categories", [])
                or any(
                    tag in preferences.get("tags", [])
                    for tag in product_data["tags"]
                )
                or product_data["brand"] in preferences.get("brands", [])
            ):
                score += 0.1
                reason_parts.append("alinha com preferências")

            if score > 0:
                recommendations.append(
                    Recommendation(
                        product_id=product_id,
                        score=round(min(score, 1.0), 2),  # Garantir máx de 1.0
                        reason=" + ".join(reason_parts),
                    )
                )

        return sorted(recommendations, key=lambda r: r.score, reverse=True)
