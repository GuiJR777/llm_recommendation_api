from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from services.recommendation_service.recommendation_service import (
    RecommendationService,
)
from services.llm.description_service import ProductDescriptionService
from services.llm.strategies.llm_emulator import LLMEmulatorStrategy

from repositories.product_repository import ProductRepository
from models.recommendation import Recommendation
from models.product import Product

from cache.redis_client import clear_all_cache

router = APIRouter()

# Serviços
recommendation_service = RecommendationService()
description_service = ProductDescriptionService(strategy=LLMEmulatorStrategy())
product_repository = ProductRepository()


# Enums
class StrategyEnum(str, Enum):
    history = "history"
    preference = "preference"


class LLMProviderEnum(str, Enum):
    emulator = "emulator"
    chatgpt = "chatgpt"


# Modelos de resposta
class RecommendationResponse(BaseModel):
    product_id: str
    score: float
    reason: str


class UserRecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[RecommendationResponse]


class DescriptionResponse(BaseModel):
    user_id: Optional[str]
    product_id: str
    personalized_description: str


# ROTAS =======================================================================


@router.get(
    "/user-recommendations/{user_id}",
    response_model=UserRecommendationResponse,
    summary="Gerar recomendações para um usuário",
    description="Retorna uma lista de produtos recomendados com score e razão, com base na estratégia especificada. Suporta filtros e paginação.",
    tags=["Recomendações"],
)
def get_user_recommendations(
    user_id: str,
    strategy: StrategyEnum = Query(
        default=StrategyEnum.history, description="Estratégia de recomendação"
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
                user_id=user_id, strategy_name=strategy.value
            )
        )

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
    "/product-description/{product_id}",
    response_model=DescriptionResponse,
    summary="Gerar descrição personalizada de produto",
    description="Gera uma descrição usando IA baseada no produto e, se informado, no usuário.",
    tags=["IA / LLM"],
)
async def generate_product_description(
    product_id: str,
    user_id: Optional[str] = None,
    llm: LLMProviderEnum = Query(
        default=LLMProviderEnum.emulator, description="Escolha do motor de LLM"
    ),
):
    try:
        if llm == LLMProviderEnum.chatgpt:
            raise HTTPException(
                status_code=501, detail="ChatGPT ainda não foi implementado"
            )

        product: Product = product_repository.get_by_id(product_id)
        description_service.set_strategy(LLMEmulatorStrategy())
        description = await description_service.describe(product, user_id)

        return DescriptionResponse(
            user_id=user_id,
            product_id=product_id,
            personalized_description=description,
        )

    except ValueError:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    except HTTPException as http_ex:
        raise http_ex
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
    summary="Limpar cache Redis",
    description="Remove todos os dados armazenados em cache de recomendações e descrições",
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
