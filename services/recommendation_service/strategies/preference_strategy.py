from services.recommendation_service.strategies.base_strategy import (
    RecommendationStrategy,
)
from models.recommendation import Recommendation
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository


class PreferenceBasedRecommendationStrategy(RecommendationStrategy):
    def __init__(self):
        self.user_repo = UserRepository()
        self.product_repo = ProductRepository()

    def recommend(self, user_id: str) -> list[Recommendation]:
        user = self.user_repo.get_by_id(user_id)
        preferred_categories = user.preferences.get("categories", [])
        preferred_tags = user.preferences.get("tags", [])
        preferred_brands = user.preferences.get("brands", [])

        purchase_prices = [
            p["price"] for p in user.purchase_history if "price" in p
        ]
        min_price = min(purchase_prices) if purchase_prices else None
        max_price = max(purchase_prices) if purchase_prices else None

        recommendations = []
        for product_data in self.product_repo.products:
            score = 0.0
            reason_parts = []

            if product_data["category"] in preferred_categories:
                score += 0.4
                reason_parts.append("categoria preferida")

            if any(tag in preferred_tags for tag in product_data["tags"]):
                score += 0.3
                reason_parts.append("tags compatíveis")

            if product_data["brand"] in preferred_brands:
                score += 0.2
                reason_parts.append("marca preferida")

            if min_price is not None and max_price is not None:
                if min_price <= product_data["price"] <= max_price:
                    score += 0.1
                    reason_parts.append("preço compatível com histórico")

            if score > 0:
                recommendations.append(
                    Recommendation(
                        product_id=product_data["id"],
                        score=round(score, 2),
                        reason=" + ".join(reason_parts),
                    )
                )

        return sorted(recommendations, key=lambda r: r.score, reverse=True)
