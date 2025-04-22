# 🧪 Modo de Desenvolvimento

Este documento contém instruções para rodar o projeto em modo de desenvolvimento, sem Docker.

---

## 🔧 Requisitos

- Python 3.10+
- Node.js 16+
- Redis local (opcional — fallback ativado)

---

## 🔌 Variáveis de ambiente

Crie um arquivo `.env` na raiz:

```env
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
CACHE_TTL_SECONDS=259200

# Se for usar OpenAI:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
```

---

## 🔁 Rodar com 3 terminais

### Terminal 1 — API principal (LLM + Recomendação)

```bash
cd llm_recommendation_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Terminal 2 — BFF (Backend for Frontend)

```bash
cd web_interface/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 3001
```

### Terminal 3 — Frontend (React)

```bash
cd web_interface/frontend
npm install
npm run dev
```

---

## 🧪 Rodando os testes

```bash
make test  # ou manualmente:
docker exec -it llm_api pytest --disable-warnings
```

### Cobertura:

```bash
pytest --cov=services --cov=models --cov=api --cov=cache
```

---

## ✨ Extras

- A navbar permite alternar entre estratégias de recomendação e motores de LLM em tempo real
- O projeto está modularizado com foco em extensão e testes