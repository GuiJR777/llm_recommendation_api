from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from services.recommendation_service.recommendation_service import (
    RecommendationService,
)
from services.llm.description_service import ProductDescriptionService
from services.llm.strategies.llm_emulator import LLMEmulatorStrategy
from services.llm.strategies.llm_chatgpt import LLMChatGPTStrategy
from repositories.product_repository import ProductRepository
from models.recommendation import Recommendation
from models.product import Product
from cache.redis_client import clear_all_cache

router = APIRouter()

# Serviços
recommendation_service = RecommendationService()
description_service = ProductDescriptionService(strategy=LLMEmulatorStrategy())

# Repositórios
product_repository = ProductRepository()


# Enums para parâmetros da URL
class StrategyEnum(str, Enum):
    history = "history"
    preference = "preference"


class LLMProviderEnum(str, Enum):
    emulator = "emulator"
    chatgpt = "chatgpt"


# Schemas de resposta
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


# ROTAS =========================================================================


@router.get(
    "/user-recommendations/{user_id}",
    response_model=UserRecommendationResponse,
    summary="Recomendações para um usuário",
    description="""
Gera uma lista de recomendações de produtos com base no usuário informado.

Você pode escolher entre duas estratégias:
- **history**: baseada no histórico de compras
- **preference**: baseada nas preferências explícitas do usuário

Além disso, é possível filtrar por `min_score`, e paginar com `limit` e `offset`.
""",
    tags=["Recomendações"],
)
def get_user_recommendations(
    user_id: str,
    strategy: StrategyEnum = Query(default=StrategyEnum.history),
    min_score: float = Query(default=0.0, ge=0.0, le=1.0),
    limit: int = Query(default=10, gt=0, le=100),
    offset: int = Query(default=0, ge=0),
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
                    product_id=r.product_id,
                    score=r.score,
                    reason=r.reason,
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
    summary="Descrição personalizada de produto com IA",
    description="""
Gera uma descrição detalhada de um produto utilizando IA Generativa.

Se um `user_id` for informado, a descrição será personalizada com base no perfil do usuário.
Você também pode escolher qual motor de IA utilizar (emulador local ou ChatGPT via OpenAI).
""",
    tags=["IA / LLM"],
)
async def generate_product_description(
    product_id: str,
    user_id: Optional[str] = None,
    llm: LLMProviderEnum = Query(default=LLMProviderEnum.emulator),
):
    try:
        match llm:
            case LLMProviderEnum.emulator:
                description_service.set_strategy("emulator")
            case LLMProviderEnum.chatgpt:
                description_service.set_strategy("chatgpt")
            case _:
                raise HTTPException(
                    status_code=501, detail="LLM não implementado"
                )

        product: Product = product_repository.get_by_id(product_id)
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
    tags=["Infraestrutura"],
    summary="Verificar se o serviço está online",
    description="Retorna o status de saúde da API.",
)
def health_check():
    return {"status": "ok"}


@router.delete(
    "/cache",
    summary="Limpar cache",
    description="Remove todo o conteúdo armazenado em cache (recomendações e descrições geradas).",
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
