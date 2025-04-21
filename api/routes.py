from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from services.recommendation_service.recommendation_service import (
    RecommendationService,
)
from models.recommendation import Recommendation
from cache.redis_client import clear_all_cache

router = APIRouter()
recommendation_service = RecommendationService()


class RecommendationResponse(BaseModel):
    product_id: str
    score: float
    reason: str


class UserRecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[RecommendationResponse]


@router.get(
    "/user-recommendations/{user_id}",
    response_model=UserRecommendationResponse,
    summary="Gerar recomendações para um usuário",
    description="Retorna uma lista de produtos recomendados com score e razão, com base na estratégia especificada. Suporta filtros e paginação.",
    tags=["Recomendações"],
)
def get_user_recommendations(
    user_id: str,
    strategy: str = Query(
        default="history",
        enum=["history", "preference"],
        description="Estratégia de recomendação",
    ),
    min_score: float = Query(
        default=0.0, ge=0.0, le=1.0, description="Score mínimo de recomendação"
    ),
    limit: int = Query(
        default=10, gt=0, le=100, description="Número máximo de recomendações"
    ),
    offset: int = Query(
        default=0, ge=0, description="Número de itens a pular no início"
    ),
):
    try:
        recommendations: list[Recommendation] = (
            recommendation_service.recommend_for_user(
                user_id=user_id, strategy_name=strategy
            )
        )

        # Filtro e paginação
        filtered = [r for r in recommendations if r.score >= min_score]
        paginated = filtered[offset : offset + limit]

        return UserRecommendationResponse(
            user_id=user_id,
            recommendations=[
                RecommendationResponse(
                    product_id=r.product_id, score=r.score, reason=r.reason
                )
                for r in paginated
            ],
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get(
    "/health-check",
    summary="Health check da API",
    description="Endpoint simples para verificar se a API está no ar.",
    tags=["Infraestrutura"],
)
def health_check():
    return {"status": "ok"}


@router.delete(
    "/cache",
    summary="Limpar cache de recomendações",
    description="Remove todos os dados armazenados em cache de recomendações",
    tags=["Infraestrutura"],
)
def clear_cache():
    try:
        clear_all_cache()
        return {"status": "cache limpo"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao limpar o cache: {str(e)}"
        )
