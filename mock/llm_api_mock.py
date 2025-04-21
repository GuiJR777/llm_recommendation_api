"""
LLM API Mock - Simulador de API de Large Language Model

Este módulo simula respostas de uma API de LLM para ser usado
durante o desenvolvimento e testes da avaliação técnica.
"""

import random
import time
import json
from typing import Dict, List, Optional, Union, Any


class LLMApiMock:
    def __init__(self):
        # Templates pré-definidos para diferentes tipos de prompts
        self.templates = {
            "product_description": {
                "generic": [
                    "O produto {{name}} é uma excelente escolha para quem busca {{category}}. Com {{feature1}} e {{feature2}}, oferece {{benefit}} para diversos usuários.",
                    "Conheça o {{name}}, projetado para oferecer a melhor experiência em {{category}}. Destacando-se por {{feature1}}, proporciona {{benefit}} incomparável.",
                    "{{name}} representa o que há de melhor em {{category}}. Suas características como {{feature1}} e {{feature2}} garantem {{benefit}} excepcional.",
                ],
                "personalized": [
                    "Baseado no seu histórico de compras, este {{name}} seria perfeito para você! Com {{feature1}} e {{feature2}}, complementa idealmente os produtos que você já possui.",
                    "Como sabemos que você aprecia {{preference}}, este {{name}} foi selecionado especialmente para você. Seu {{feature1}} combina perfeitamente com seu estilo.",
                    "Este {{name}} foi escolhido pensando em você! Com {{feature1}}, é ideal para seu interesse em {{preference}} e complementa sua coleção de {{category}}.",
                ],
            },
            "recommendation_explanation": [
                "Este produto foi recomendado porque se alinha com seu gosto por {{preference}} e complementa perfeitamente sua compra recente de {{recent_purchase}}.",
                "Baseado em suas compras anteriores, especialmente {{recent_purchase}}, acreditamos que você vai adorar este item com {{feature1}}.",
                "Clientes que compraram {{recent_purchase}} como você frequentemente ficam satisfeitos com este produto devido ao seu {{feature1}} excepcional.",
            ],
            "product_comparison": [
                "Comparando {{product1}} e {{product2}}, o primeiro se destaca em {{feature1}}, enquanto o segundo oferece melhor {{feature2}}. Para seu uso em {{usage}}, recomendamos {{recommendation}}.",
                "Entre {{product1}} e {{product2}}, você encontrará diferenças significativas em {{feature1}} e {{feature2}}. Considerando sua preferência por {{preference}}, {{recommendation}} seria mais adequado.",
                "{{product1}} e {{product2}} têm abordagens diferentes para {{category}}. O primeiro prioriza {{feature1}}, o segundo foca em {{feature2}}. Para seu caso específico, {{recommendation}} oferece mais vantagens.",
            ],
            "error_responses": [
                "Desculpe, não foi possível gerar uma descrição personalizada neste momento. Por favor, tente novamente mais tarde.",
                "Ocorreu um erro ao processar sua solicitação. Nossa equipe foi notificada e está trabalhando para resolver o problema.",
                "Estamos enfrentando dificuldades técnicas temporárias. Por favor, utilize as descrições padrão disponíveis enquanto resolvemos esta questão.",
            ],
        }

        # Banco de dados simulado de preferências de usuários
        self.user_preferences = {
            "u1001": {
                "preferences": ["eletrônicos", "tecnologia", "gadgets"],
                "recent_purchases": ["smartphone", "fones de ouvido"],
                "style": "técnico e detalhado",
            },
            "u1002": {
                "preferences": ["moda", "beleza", "acessórios"],
                "recent_purchases": ["vestido casual", "kit maquiagem"],
                "style": "elegante e moderno",
            },
            "u1003": {
                "preferences": ["eletrônicos", "esportes", "ferramentas"],
                "recent_purchases": ["notebook", "monitor gamer"],
                "style": "direto e técnico",
            },
            "u1004": {
                "preferences": ["moda", "livros", "decoração"],
                "recent_purchases": ["bolsa tote", "óculos de sol"],
                "style": "casual e descontraído",
            },
            "u1005": {
                "preferences": [
                    "eletrônicos",
                    "ferramentas",
                    "utensílios domésticos",
                ],
                "recent_purchases": ["smart tv", "furadeira"],
                "style": "prático e objetivo",
            },
        }

        # Banco de dados simulado de características de produtos
        self.product_features = {
            "p1005": {
                "name": "Fones de Ouvido Bluetooth TechMaster Pro",
                "category": "áudio",
                "feature1": "cancelamento de ruído ativo",
                "feature2": "até 20 horas de bateria",
                "benefit": "som imersivo e conforto duradouro",
            },
            "p2001": {
                "name": "Notebook TechMaster Pro",
                "category": "computadores",
                "feature1": "processador Intel i7",
                "feature2": "placa de vídeo dedicada",
                "benefit": "performance excepcional para trabalho e jogos",
            },
            "p3001": {
                "name": "Conjunto de Panelas HomeComfort Premium",
                "category": "utensílios de cozinha",
                "feature1": "revestimento antiaderente",
                "feature2": "cabo removível",
                "benefit": "praticidade e durabilidade na cozinha",
            },
            "p6001": {
                "name": "Vestido Casual StylePlus",
                "category": "moda feminina",
                "feature1": "tecido de algodão premium",
                "feature2": "corte moderno",
                "benefit": "conforto e estilo para o dia a dia",
            },
            "p7001": {
                "name": "Sabonete Facial BeautyEssence",
                "category": "cuidados com a pele",
                "feature1": "extrato de chá verde",
                "feature2": "fórmula suave",
                "benefit": "limpeza profunda sem ressecar",
            },
        }

        # Carrega mais produtos do arquivo se disponível
        try:
            with open("data/products.json", "r", encoding="utf-8") as f:
                products_data = json.load(f)
                for product in products_data.get("products", []):
                    product_id = product.get("id")
                    if product_id and product_id not in self.product_features:
                        self.product_features[product_id] = {
                            "name": product.get("name", ""),
                            "category": product.get("category", ""),
                            "feature1": product.get("specifications", {}).get(
                                (
                                    list(
                                        product.get(
                                            "specifications", {}
                                        ).keys()
                                    )[0]
                                    if product.get("specifications", {})
                                    else ""
                                ),
                                "",
                            ),
                            "feature2": product.get("specifications", {}).get(
                                (
                                    list(
                                        product.get(
                                            "specifications", {}.keys()
                                        )
                                    )[1]
                                    if len(
                                        product.get(
                                            "specifications", {}
                                        ).keys()
                                    )
                                    > 1
                                    else ""
                                ),
                                "",
                            ),
                            "benefit": (
                                product.get("description", "").split(",")[0]
                                if "," in product.get("description", "")
                                else product.get("description", "")
                            ),
                        }
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            # Continua com os dados padrão se não conseguir carregar o arquivo
            pass

    async def generate_response(self, params: Dict[str, Any]) -> str:
        """
        Simula o envio de um prompt para o LLM e retorna uma resposta

        Args:
            params: Parâmetros do prompt (prompt, type, user_id, product_id, etc)

        Returns:
            Resposta simulada do LLM
        """
        # Simula latência de rede
        latency = random.randint(200, 1000) / 1000  # 200-1000ms
        time.sleep(latency)

        # Simula falha ocasional da API (5% de chance)
        if random.random() < 0.05:
            raise Exception("Simulação de falha na API do LLM")

        # Processa diferentes tipos de prompts
        response = ""

        if params.get("type") == "generic_description":
            response = self.generate_generic_description(
                params.get("product_id")
            )
        elif params.get("type") == "personalized_description":
            response = self.generate_personalized_description(
                params.get("user_id"), params.get("product_id")
            )
        elif params.get("type") == "recommendation_explanation":
            response = self.generate_recommendation_explanation(
                params.get("user_id"), params.get("product_id")
            )
        elif params.get("type") == "product_comparison":
            response = self.generate_product_comparison(
                params.get("product_ids"), params.get("user_id")
            )
        else:
            # Para prompts personalizados, analisa o texto e gera uma resposta contextual
            response = self.generate_custom_response(
                params.get("prompt", ""), params.get("user_id")
            )

        return response

    def generate_generic_description(self, product_id: str) -> str:
        """
        Gera uma descrição genérica para um produto

        Args:
            product_id: ID do produto

        Returns:
            Descrição genérica
        """
        # Verifica se temos informações sobre este produto
        product = self.product_features.get(product_id)
        if not product:
            return "Descrição não disponível para este produto."

        # Seleciona um template aleatório
        templates = self.templates["product_description"]["generic"]
        template = random.choice(templates)

        # Preenche o template com os dados do produto
        return (
            template.replace("{{name}}", product["name"])
            .replace("{{category}}", product["category"])
            .replace("{{feature1}}", product["feature1"])
            .replace("{{feature2}}", product["feature2"])
            .replace("{{benefit}}", product["benefit"])
        )

    def generate_personalized_description(
        self, user_id: str, product_id: str
    ) -> str:
        """
        Gera uma descrição personalizada de produto para um usuário específico

        Args:
            user_id: ID do usuário
            product_id: ID do produto

        Returns:
            Descrição personalizada
        """
        # Verifica se temos informações sobre este usuário e produto
        user = self.user_preferences.get(user_id)
        product = self.product_features.get(product_id)

        if not user or not product:
            return self.generate_generic_description(product_id)

        # Seleciona um template aleatório
        templates = self.templates["product_description"]["personalized"]
        template = random.choice(templates)

        # Escolhe uma preferência aleatória do usuário
        preference = random.choice(user["preferences"])

        # Preenche o template com os dados do produto e do usuário
        return (
            template.replace("{{name}}", product["name"])
            .replace("{{feature1}}", product["feature1"])
            .replace("{{feature2}}", product["feature2"])
            .replace("{{preference}}", preference)
            .replace("{{category}}", product["category"])
        )

    def generate_recommendation_explanation(
        self, user_id: str, product_id: str
    ) -> str:
        """
        Gera uma explicação para uma recomendação

        Args:
            user_id: ID do usuário
            product_id: ID do produto

        Returns:
            Explicação da recomendação
        """
        user = self.user_preferences.get(user_id)
        product = self.product_features.get(product_id)

        if not user or not product:
            return "Este produto foi recomendado com base nas tendências gerais de compra."

        # Seleciona um template aleatório
        templates = self.templates["recommendation_explanation"]
        template = random.choice(templates)

        # Escolhe uma preferência e compra recente aleatória
        preference = random.choice(user["preferences"])
        recent_purchase = random.choice(user["recent_purchases"])

        # Preenche o template
        return (
            template.replace("{{preference}}", preference)
            .replace("{{recent_purchase}}", recent_purchase)
            .replace("{{feature1}}", product["feature1"])
        )

    def generate_product_comparison(
        self, product_ids: List[str], user_id: Optional[str] = None
    ) -> str:
        """
        Gera uma comparação entre produtos

        Args:
            product_ids: IDs dos produtos a comparar
            user_id: ID do usuário (opcional)

        Returns:
            Texto de comparação
        """
        # Verifica se temos pelo menos dois produtos para comparar
        if not isinstance(product_ids, list) or len(product_ids) < 2:
            return "É necessário fornecer pelo menos dois produtos para comparação."

        product1 = self.product_features.get(product_ids[0])
        product2 = self.product_features.get(product_ids[1])

        if not product1 or not product2:
            return "Não foi possível comparar os produtos selecionados."

        # Seleciona um template aleatório
        templates = self.templates["product_comparison"]
        template = random.choice(templates)

        # Determina uma recomendação baseada em preferências do usuário (se disponível)
        recommendation = product1["name"]
        preference = product1["category"]
        usage = "dia a dia"

        if user_id and user_id in self.user_preferences:
            user = self.user_preferences[user_id]
            preference = user["preferences"][0]

            # Recomendação simplificada baseada em preferências
            if product1["category"] in user["preferences"]:
                recommendation = product1["name"]
            elif product2["category"] in user["preferences"]:
                recommendation = product2["name"]

        # Preenche o template
        return (
            template.replace("{{product1}}", product1["name"])
            .replace("{{product2}}", product2["name"])
            .replace("{{feature1}}", product1["feature1"])
            .replace("{{feature2}}", product2["feature2"])
            .replace("{{preference}}", preference)
            .replace("{{usage}}", usage)
            .replace("{{recommendation}}", recommendation)
            .replace("{{category}}", product1["category"])
        )

    def generate_custom_response(
        self, prompt: str, user_id: Optional[str] = None
    ) -> str:
        """
        Gera uma resposta para um prompt personalizado

        Args:
            prompt: Texto do prompt
            user_id: ID do usuário (opcional)

        Returns:
            Resposta gerada
        """
        # Análise simples do prompt para determinar o contexto
        lower_prompt = prompt.lower()

        # Verifica se é uma solicitação de recomendação
        if "recomend" in lower_prompt or "sugest" in lower_prompt:
            if user_id and user_id in self.user_preferences:
                user = self.user_preferences[user_id]
                preference = user["preferences"][0]
                return f"Com base no seu interesse em {preference}, recomendamos produtos da categoria {preference} que complementariam suas compras recentes. Especialmente itens com características similares aos que você já adquiriu, mas com funcionalidades adicionais ou design atualizado."
            else:
                return "Baseado nas tendências atuais, recomendamos explorar produtos das categorias mais populares como eletrônicos, moda e decoração. Produtos com boas avaliações e descontos são sempre uma escolha confiável."

        # Verifica se é uma solicitação de descrição
        if (
            "descri" in lower_prompt
            or "detalh" in lower_prompt
            or "explic" in lower_prompt
        ):
            return "Uma descrição eficaz destaca os benefícios principais do produto, suas características distintas e como ele atende às necessidades do cliente. A personalização deve considerar o histórico de compras, interesses manifestados e comportamento de navegação do usuário."

        # Resposta padrão para outros tipos de prompts
        return "Entendo sua solicitação. Para oferecer a melhor experiência, recomendamos utilizar nossos templates específicos para descrições de produtos, comparações, ou explicações de recomendações. Isso permite que nossa IA gere conteúdo mais relevante e personalizado para seus clientes."


# Exemplo de uso
if __name__ == "__main__":
    import asyncio

    async def test_llm():
        llm_api = LLMApiMock()

        try:
            # Descrição genérica de produto
            generic_desc = await llm_api.generate_response(
                {"type": "generic_description", "product_id": "p1005"}
            )
            print("Descrição genérica:", generic_desc)

            # Descrição personalizada
            personalized_desc = await llm_api.generate_response(
                {
                    "type": "personalized_description",
                    "user_id": "u1001",
                    "product_id": "p1005",
                }
            )
            print("Descrição personalizada:", personalized_desc)

            # Explicação de recomendação
            recommendation_exp = await llm_api.generate_response(
                {
                    "type": "recommendation_explanation",
                    "user_id": "u1002",
                    "product_id": "p7001",
                }
            )
            print("Explicação de recomendação:", recommendation_exp)

            # Comparação de produtos
            comparison = await llm_api.generate_response(
                {
                    "type": "product_comparison",
                    "product_ids": ["p1005", "p2001"],
                    "user_id": "u1003",
                }
            )
            print("Comparação de produtos:", comparison)

            # Prompt personalizado
            custom_response = await llm_api.generate_response(
                {
                    "prompt": "Como posso gerar recomendações eficazes?",
                    "user_id": "u1001",
                }
            )
            print("Resposta personalizada:", custom_response)

        except Exception as e:
            print("Erro:", str(e))

    # Executa o exemplo
    asyncio.run(test_llm())
