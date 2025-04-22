# Prompt templates para o LLMChatGPTStrategy

GENERIC_SYSTEM_PROMPT = "Você é uma IA especialista em ecommerce e irá gerar descrições atrativas para produtos com base em suas características."

GENERIC_USER_PROMPT = """
Gere uma descrição detalhada e atrativa para o seguinte produto:

Nome: {name}
Categoria: {category} / {sub_category}
Marca: {brand}
Descrição base: {description}
Tags: {tags}
Especificações:
{specs}

Gere uma descrição neutra, mas envolvente, com linguagem clara e comercial.
"""

PERSONALIZED_USER_PROMPT = """
Gere uma descrição personalizada para o produto abaixo, levando em consideração o perfil do usuário:

Produto:
- Nome: {name}
- Categoria: {category} / {sub_category}
- Marca: {brand}
- Descrição base: {description}
- Tags: {tags}
- Especificações:
{specs}

Usuário:
- Nome: {user_name}
- Idade: {age}
- Gênero: {gender}
- Localização: {location}
- Categorias preferidas: {pref_categories}
- Marcas preferidas: {pref_brands}
- Faixa de preço: {price_range}
- Histórico de compras: {purchased_products}

Crie uma descrição persuasiva adaptando o tom e os benefícios para o perfil do usuário. Evite repetir literalmente a descrição base. Use uma linguagem natural, clara e comercial.
"""
