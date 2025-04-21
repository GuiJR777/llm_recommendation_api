# Recommender System with LLM (Mock)

Este projeto é uma solução para um desafio técnico que envolve:

- Sistema de recomendação baseado em histórico de comportamento do usuário
- Integração com IA Generativa via simulador LLM
- API RESTful com FastAPI
- Arquitetura modular seguindo princípios SOLID
- Estratégias intercambiáveis com uso do padrão Strategy
- Fallback automático para descrições genéricas
- Cache com Redis (com fallback)
- Testes unitários com cobertura total usando fakeredis
- Ambientes separados com `requirements.txt` e `requirements-dev.txt`

---

## 🚀 Como rodar a aplicação

### 1. Instale as dependências de produção:
```bash
pip install -r requirements.txt
```

### 2. Para ambiente de desenvolvimento/testes:
```bash
pip install -r requirements-dev.txt
```

### 3. Crie um arquivo `.env` na raiz com o seguinte conteúdo:
```dotenv
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
CACHE_TTL_SECONDS=259200  # 72h
```

### 4. Inicie o servidor FastAPI:
```bash
uvicorn main:app --reload
```

### 5. Acesse a documentação interativa:
```
http://localhost:8000/docs
```

---

## ⚙️ Configuração do Redis via `.env`

Este projeto utiliza o Redis como mecanismo de cache. As variáveis de ambiente são carregadas via `python-dotenv`.

### Exemplo de `.env`:
```dotenv
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
CACHE_TTL_SECONDS=259200
```

> ℹ️ Se o Redis não estiver disponível, o sistema continuará funcionando normalmente, apenas sem cache.

---

## ✅ Sobre os testes

Este projeto segue uma abordagem rigorosa para testes unitários com cobertura próxima de 100%. As principais regras adotadas são:

- Estrutura de pastas espelhada (`tests/` acompanha a árvore do projeto)
- Um arquivo de teste por classe
- Cada método testado possui uma `TestClass` com múltiplos métodos `test_if_should...`
- Estilo AAA (Arrange, Act, Assert)
- Sem lógica condicional (sem `if`, `for`, etc.)
- Linhas com mais de 79 caracteres usam `# noqa`
- Cache testado com `fakeredis`, sem necessidade de Redis real

---

## 🧠 Estratégias de recomendação para usuários

O sistema usa o padrão **Strategy** para alternar dinamicamente entre algoritmos de recomendação.

### 1. `HistoryBasedRecommendationStrategy`

Baseado no comportamento histórico do usuário. A pontuação usa os seguintes pesos:

| Fonte                   | Peso |
|------------------------|------|
| `purchase_history`     | 0.4  |
| `cart_events`          | 0.3  |
| `browsing_history`     | 0.2  |
| `match with preferences` | 0.1 |

O resultado inclui um campo `reason` indicando o motivo da recomendação.

---

### 2. `PreferenceBasedRecommendationStrategy`

Baseado nas preferências explícitas do usuário:

- Categorias favoritas
- Marcas preferidas
- Tags associadas
- Faixa de preço observada no histórico

| Fator                  | Peso |
|------------------------|------|
| Categoria preferida    | 0.4  |
| Tags compatíveis       | 0.3  |
| Marca preferida        | 0.2  |
| Faixa de preço         | 0.1  |

---

## 🤖 Geração de descrições com IA (LLM)

O sistema possui um serviço dedicado para gerar descrições de produtos utilizando motores LLM intercambiáveis.

### ✨ Endpoint:

```
GET /product-description/{product_id}?user_id={user_id}&llm={motor}
```

- `product_id` (obrigatório)
- `user_id` (opcional)
- `llm` (default: `emulator`)

### LLMs disponíveis:

| Valor     | Estratégia utilizada                          |
|-----------|-----------------------------------------------|
| `emulator` | Mock simulado com `LLMEmulatorStrategy`       |
| `chatgpt`  | **Em breve**: integração real com OpenAI ChatGPT |

> ⚠️ Caso use um `llm` ainda não implementado, a API retorna `501 - Not Implemented`.

### Exemplo de resposta:

```json
{
  "user_id": "u1001",
  "product_id": "p1025",
  "personalized_description": "Este Tablet TechMaster Tab é perfeito para você que prioriza eletrônicos de qualidade..."
}
```

As descrições são armazenadas em cache automaticamente por 72h.

---

## 🧪 Rodando os testes

```bash
pytest --disable-warnings
```

> ✅ Recomendado usar `requirements-dev.txt` para ter suporte ao `fakeredis`, `pytest-asyncio` e outras libs de teste.

---

## 📊 Geração de cobertura de testes

```bash
pip install pytest-cov
pytest --cov=services --cov=models --cov=api --cov=cache
```
