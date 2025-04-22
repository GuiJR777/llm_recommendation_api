import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch

client = TestClient(app)


class TestHealthCheck:
    def test_if_should_return_status_ok(self):
        response = client.get("/health-check")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestUserRecommendations:
    def test_if_should_return_recommendations_default(self):
        response = client.get("/user-recommendations/u1001")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)
        assert len(data["recommendations"]) > 0

    def test_if_should_return_recommendations_with_preference_strategy(self):
        response = client.get(
            "/user-recommendations/u1001?strategy=preference"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "u1001"
        assert all("reason" in r for r in data["recommendations"])

    def test_if_should_filter_by_min_score(self):
        response = client.get("/user-recommendations/u1001?min_score=0.9")
        assert response.status_code == 200
        scores = [r["score"] for r in response.json()["recommendations"]]
        assert all(score >= 0.9 for score in scores)

    def test_if_should_limit_and_offset_results(self):
        full = client.get("/user-recommendations/u1001").json()[
            "recommendations"
        ]
        paginated = client.get(
            "/user-recommendations/u1001?limit=2&offset=1"
        ).json()["recommendations"]
        assert len(paginated) == 2
        assert paginated[0] == full[1]
        assert paginated[1] == full[2]

    def test_if_invalid_user_should_return_404(self):
        response = client.get("/user-recommendations/invalid_user")
        assert response.status_code == 404
        assert "detail" in response.json()

    def test_if_invalid_strategy_should_return_422(self):
        response = client.get("/user-recommendations/u1001?strategy=unknown")
        assert response.status_code == 422


class TestProductDescriptionRoute:
    @patch(
        "services.llm.strategies.llm_chatgpt.LLMChatGPTStrategy.generate_description",
        new_callable=AsyncMock,
    )
    def test_if_chatgpt_should_return_200(self, mock_generate):
        mock_generate.return_value = "Mocked description!"

        response = client.get("/product-description/p1005?llm=chatgpt")

        assert response.status_code == 200
        assert "personalized_description" in response.json()
        assert (
            response.json()["personalized_description"]
            == "Mocked description!"
        )

    @patch(
        "services.llm.strategies.llm_chatgpt.LLMChatGPTStrategy.generate_description",
        new_callable=AsyncMock,
    )
    def test_if_chatgpt_with_error_should_fallback(self, mock_generate):
        mock_generate.side_effect = Exception("Unauthorized")

        response = client.get("/product-description/p1005?llm=chatgpt")

        assert response.status_code == 200
        assert "personalized_description" in response.json()
        assert isinstance(response.json()["personalized_description"], str)

    def test_if_should_return_personalized_description(self):
        response = client.get(
            "/product-description/p1005?user_id=u1001&llm=emulator"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == "p1005"
        assert data["user_id"] == "u1001"
        assert isinstance(data["personalized_description"], str)
        assert len(data["personalized_description"]) > 10

    def test_if_should_return_generic_description_without_user(self):
        response = client.get("/product-description/p1005")
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == "p1005"
        assert data["user_id"] is None
        assert isinstance(data["personalized_description"], str)

    def test_if_invalid_product_should_return_404(self):
        response = client.get("/product-description/invalid123")
        assert response.status_code == 404
        assert "Produto não encontrado" in response.json()["detail"]

    def test_if_invalid_llm_should_return_422(self):
        response = client.get("/product-description/p1005?llm=banana")
        assert response.status_code == 422  # Validação automática do Enum


class TestCacheEndpoint:
    def test_if_should_clear_cache_successfully(self):
        response = client.delete("/cache")
        assert response.status_code == 200
        assert response.json()["status"] == "cache limpo"
