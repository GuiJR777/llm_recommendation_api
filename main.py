from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(
    title="Recommender API with LLM",
    version="1.0.0",
    description="""
API RESTful para recomendação de produtos com geração de descrições usando LLMs.

**Funcionalidades:**
- Recomendação de produtos por histórico ou preferências
- Descrições geradas com IA generativa (ChatGPT ou simulador)
- Cache automático com Redis
- Suporte a múltiplos motores LLM com fallback

Documentação interativa disponível em /docs.
""",
    openapi_tags=[
        {"name": "IA / LLM", "description": "Endpoints para geração com LLM"},
        {
            "name": "Recomendações",
            "description": "Endpoints de recomendação de produtos",
        },
        {
            "name": "Infraestrutura",
            "description": "Endpoints de infraestrutura e cache",
        },
    ],
)

app.include_router(api_router)
