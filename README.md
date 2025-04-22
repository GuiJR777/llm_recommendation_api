# 🧠 Recommender System with LLM (Desafio Técnico)

Este projeto é uma solução completa envolvendo:

- ✅ Sistema de recomendação com múltiplas estratégias (Strategy Pattern)
- 🤖 Geração de descrições de produtos usando IA generativa (LLMs)
- 🚀 API RESTful com FastAPI e documentação automática (Swagger)
- 📦 Cache inteligente com Redis e fallback
- 🔍 Logging estruturado
- ✅ Testes unitários com cobertura quase total
- 🧪 Ambiente de testes com `fakeredis`, `pytest` e `pytest-asyncio`
- 🌐 Interface em React com configuração dinâmica de estratégias

---

## 🚀 Como rodar a aplicação

Clone esse repositório e depois:

### Configure variáveis de ambiente em um arquivo `.env`:
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

Use **três terminais separados** para rodar cada serviço:

---

### 🔵 1. API Principal (LLM + Recomendação)

```bash
cd llm_recommendation_api
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

> Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🟢 2. API BFF (Backend for Frontend)

```bash
source venv/bin/activate
cd web_interface/backend
uvicorn main:app --reload --port 3001
```

> Essa API serve os dados da pasta `data/` para o frontend

---

### 🟣 3. Frontend React

```bash
cd web_interface/frontend
npm install
npm run dev
```

> Acesse: [http://localhost:5173](http://localhost:5173)

---

## ⚙️ Estratégias configuráveis

Na **navbar** é possível escolher dinamicamente:

- Estratégia de recomendação: `history` ou `preference`
- Motor de descrição: `emulator` ou `chatgpt`

Essas configurações afetam diretamente as chamadas de API do sistema.

---

## 🌐 Endpoints das APIs

### API Principal (porta 8000)
- `GET /user-recommendations/{user_id}?strategy=...`
- `GET /product-description/{product_id}?user_id=...&llm=...`

### API BFF (porta 3001)
- `GET /api/users`
- `GET /api/users/{user_id}`
- `GET /api/products`
- `GET /api/products/{product_id}`

---

## ⚙️ Funcionalidades principais

### 🔁 Estratégias de Recomendação (Strategy Pattern)

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

As descrições são geradas por um LLM, com cache automático de 24h via Redis.

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

> Testes usam `fakeredis` para simular Redis local.

#### Cobertura:

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

O projeto segue princípios **SOLID**, separação de responsabilidades e foi projetado com foco em:

- 🔁 Extensibilidade (novas estratégias ou LLMs)
- 🧪 Testabilidade (mock e cobertura)
- 🧘 Manutenibilidade (modular e limpo)

---

## ✨ Diferenciais

- ✅ Cache com TTL customizável
- ✅ Fallback automático
- ✅ Logging estruturado
- ✅ Documentação Swagger
- ✅ Interface em React integrada com as APIs

---

## 📁 Estrutura do projeto

```
llm_recommendation_api/
├── main.py
├── models/
├── services/
├── strategies/
├── data/
└── tests/

web_interface/
├── backend/
│   └── FastAPI (porta 3001)
├── frontend/
│   └── React + Vite (porta 5173)
```

---

## ✅ Pré-requisitos

- Python 3.10+
- Node.js 16+
- Redis (opcional — fallback automático)