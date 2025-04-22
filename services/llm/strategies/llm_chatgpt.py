import openai
from typing import Optional
from models.product import Product
from models.user import User
from services.llm.strategies.llm_strategy import LLMStrategy
from repositories.user_repository import UserRepository
from utils.config import OPENAI_API_KEY, OPENAI_MODEL
from utils.logger import logger
from services.llm.strategies import llm_chatgpt_templates as templates


class LLMChatGPTStrategy(LLMStrategy):
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada no .env")

        self.client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.user_repo = UserRepository()

    async def generate_description(
        self, product: Product, user_id: Optional[str] = None
    ) -> str:
        try:
            user_msg = (
                self._build_personalized_prompt(product, user_id)
                if user_id
                else self._build_generic_prompt(product)
            )

            logger.info(
                f"[ChatGPT Request] model={self.model}, user_id={user_id}, product_id={product.id}"  # noqa
            )
            logger.debug(f"[ChatGPT Prompt] {user_msg}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": templates.GENERIC_SYSTEM_PROMPT,
                    },
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.8,
                max_tokens=300,
            )

            message = response.choices[0].message.content.strip()
            logger.info(
                f"[ChatGPT Response] product_id={product.id}, user_id={user_id}"  # noqa
            )
            logger.debug(f"[ChatGPT Message] {message}")
            return message

        except Exception as e:
            logger.exception(
                f"[ChatGPT Error] product_id={product.id}, user_id={user_id}, error={e}"  # noqa
            )
            logger.warning("[ChatGPT Fallback] Usando descrição genérica.")
            return self._fallback_description(product)

    def _build_generic_prompt(self, product: Product) -> str:
        return templates.GENERIC_USER_PROMPT.format(
            name=product.name,
            category=product.category,
            sub_category=product.sub_category,
            brand=product.brand,
            description=product.description,
            tags=", ".join(product.tags),
            specs=self._format_specs(product.specifications),
        )

    def _build_personalized_prompt(
        self, product: Product, user_id: str
    ) -> str:
        try:
            user: User = self.user_repo.get_by_id(user_id)
        except Exception as e:
            logger.warning(f"[ChatGPT] Usuário {user_id} não encontrado: {e}")
            return self._build_generic_prompt(product)

        return templates.PERSONALIZED_USER_PROMPT.format(
            name=product.name,
            category=product.category,
            sub_category=product.sub_category,
            brand=product.brand,
            description=product.description,
            tags=", ".join(product.tags),
            specs=self._format_specs(product.specifications),
            user_name=user.name,
            age=user.age,
            gender=user.gender,
            location=user.location,
            pref_categories=", ".join(user.preferences["categories"]),
            pref_brands=", ".join(user.preferences["brands"]),
            price_range=user.preferences["price_range"],
            purchased_products=", ".join(
                p["product_id"] for p in user.purchase_history
            ),
        )

    def _format_specs(self, specs: dict) -> str:
        return "\n".join([f"- {k}: {v}" for k, v in specs.items()])

    def _fallback_description(self, product: Product) -> str:
        return (
            f"{product.name} é um produto da categoria {product.category} que oferece "  # noqa
            f"{product.description}. Ideal para quem busca qualidade e praticidade."  # noqa
        )
