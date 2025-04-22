# 🧠 Recommender System with LLM (Desafio Técnico)

Este projeto é uma solução para um desafio técnico envolvendo:

- ✅ Sistema de recomendação com múltiplas estratégias (Strategy Pattern)
- 🤖 Geração de descrições de produtos usando IA generativa (LLMs)
- 🚀 API RESTful com FastAPI e documentação automática (Swagger)
- 📦 Cache inteligente com Redis e fallback
- 🔍 Logging estruturado
- ✅ Testes unitários com cobertura quase total
- 🧪 Ambiente de testes com `fakeredis`, `pytest` e `pytest-asyncio`

---

## 🚀 Como rodar a aplicação

### 1. Clone o repositório:
```bash
git clone https://github.com/GuiJR777/llm_recommendation_api.git
cd llm_recommendation_api
```

### 2. Verifique a versão do Python:
Este projeto requer **Python 3.10 ou superior**.
```bash
python --version
```

### 3. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 4. Instale as dependências de produção:
```bash
pip install -r requirements.txt
```

### 5. Ou instale dependências de desenvolvimento/teste:
```bash
pip install -r requirements-dev.txt
```

### 6. Configure variáveis de ambiente em um arquivo `.env`:
```dotenv
# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
CACHE_TTL_SECONDS=259200  # 72h

# OpenAI (opcional)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
```

### 7. Inicie o servidor local:
```bash
uvicorn main:app --reload
```

### 8. Acesse a documentação da API:
- 📘 Swagger UI: http://localhost:8000/docs
- 📄 OpenAPI JSON: http://localhost:8000/openapi.json

---

## ⚙️ Funcionalidades principais

### 🔁 Estratégias de Recomendação (Strategy Pattern)

O sistema permite alternar entre múltiplas estratégias de recomendação:

#### `HistoryBasedRecommendationStrategy`

| Fonte                     | Peso |
|--------------------------|------|
| Histórico de compras     | 0.4  |
| Eventos no carrinho      | 0.3  |
| Histórico de navegação   | 0.2  |
| Afinidade com preferências | 0.1 |

#### `PreferenceBasedRecommendationStrategy`

| Fator                   | Peso |
|------------------------|------|
| Categoria preferida    | 0.4  |
| Tags associadas        | 0.3  |
| Marca preferida        | 0.2  |
| Faixa de preço         | 0.1  |

---

### 🤖 Geração de descrições com IA

As descrições são geradas por uma LLM (IA Generativa), com cache por 24h via Redis.

#### Endpoint:
```
GET /product-description/{product_id}?user_id={user_id}&llm={motor}
```

#### Parâmetros:
- `product_id` (obrigatório)
- `user_id` (opcional) — para personalização
- `llm`: `emulator` (mock) ou `chatgpt` (real via OpenAI)

#### Exemplo de resposta:
```json
{
  "user_id": "u1001",
  "product_id": "p1025",
  "personalized_description": "Este Tablet TechMaster Tab é perfeito para quem valoriza performance com praticidade..."
}
```

---

### 🧪 Testes

```bash
pytest --disable-warnings
```

> Testes utilizam `fakeredis` para simular Redis sem dependência externa.

#### Geração de cobertura:
```bash
pytest --cov=services --cov=models --cov=api --cov=cache
```

---

### 🛠️ Endpoints principais

| Método | Rota                                | Descrição                                         |
|--------|-------------------------------------|--------------------------------------------------|
| GET    | `/user-recommendations/{user_id}`  | Lista produtos recomendados para um usuário     |
| GET    | `/product-description/{product_id}`| Gera descrição com IA para o produto            |
| GET    | `/health-check`                    | Verifica status da API                          |
| DELETE | `/cache`                           | Limpa todos os dados de cache                   |

---

## 💬 Considerações

O projeto segue princípios **SOLID**, separação de responsabilidades, e foi projetado com foco em:

- 🔁 Extensibilidade (novas estratégias de recomendação ou LLMs)
- 🧪 Testabilidade (mock e cobertura)
- 🧘 Manutenibilidade (modular e limpo)

---

## ✨ Diferenciais

- ✅ Cache com TTL customizável
- ✅ Fallback automático para IA e recomendações
- ✅ Logging estruturado para auditoria de chamadas ao LLM
- ✅ Documentação Swagger pronta para API pública

---

## 📁 Estrutura do projeto

```
.
├── api/                  # Rotas e endpoints
├── services/             # Lógicas de negócio (Recomendações e LLM)
├── models/               # Entidades Pydantic
├── repositories/         # Acesso a dados fake
├── cache/                # Cache Redis + Decorators
├── tests/                # Testes unitários
├── main.py               # Entry point
├── requirements.txt
└── .env
```