# 🧠 Recommender System with LLM

Este projeto é uma solução completa envolvendo:

- ✅ Sistema de recomendação baseado em múltiplas estratégias (Strategy Pattern)
- 🤖 Geração de descrições de produtos com IA Generativa (LLM ou mock)
- 🧪 Testes unitários com cobertura quase total
- 🌐 Interface React moderna e dinâmica (com troca de estratégia em tempo real)
- 🐳 Docker e Makefile para execução oficial com um único comando

---

## 📥 Clonando o projeto

```bash
git clone https://github.com/GuiJR777/llm_recommendation_api.git
cd llm_recommendation_api
```

---

## 🚀 Como rodar (modo oficial com Docker + Makefile)

### 📦 Pré-requisitos

- Docker
- Docker Compose
- `make` (no Linux ou WSL no Windows)

### ▶️ Comando principal

```bash
make up
```

> Esse comando sobe todos os serviços: frontend + backend + API principal + Redis

### ✅ Serviços disponíveis

| Serviço       | Porta | Descrição                                 |
|---------------|-------|--------------------------------------------|
| `frontend`    | 80    | Interface React via NGINX                  |
| `llm_api`     | 8000  | API principal com recomendação e IA LLM    |
| `bff_api`     | 3001  | API intermediária que expõe os dados JSON  |
| `redis`       | 6379  | Cache TTL com fallback automático          |

Acesse:

- Frontend: [http://localhost](http://localhost)
- API principal: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Comandos úteis com `make`

| Comando            | Descrição                                     |
|--------------------|-----------------------------------------------|
| `make up`          | Sobe todos os serviços                        |
| `make down`        | Derruba os containers                         |
| `make build`       | Rebuilda manualmente todos os serviços        |
| `make logs`        | Mostra logs em tempo real                     |
| `make shell-api`   | Entra no container da API principal           |
| `make shell-bff`   | Entra no container da API BFF                 |
| `make test`        | Executa testes da API principal               |
| `make reset-cache` | Chama a rota que limpa o Redis por endpoint   |

---

## 🧱 Arquitetura

```
.
├── main.py
├── requirements.txt
├── docker-compose.yml
├── Makefile
├── .dockerignore
├── .env
├── models/
├── services/
├── strategies/
└── web_interface/
    ├── backend/  ← API BFF (FastAPI)
    |   |
    |   └── data/ ← Usuários e produtos (JSON)
    |
    └── frontend/ ← Interface React (Vite + NGINX)

```

---

## 🤖 IA Generativa (LLM)

A descrição dos produtos pode ser gerada com dois motores:

| Motor      | Descrição                            |
|------------|--------------------------------------|
| `emulator` | Mock local simulado para testes      |
| `chatgpt`  | Integração real com OpenAI (opcional)|

### Endpoint

```http
GET /product-description/{product_id}?user_id={user_id}&llm=chatgpt
```

---

## 📊 Estratégias de recomendação

| Estratégia | Lógica                                               |
|------------|------------------------------------------------------|
| `history`  | Baseado em compras, navegação e carrinho             |
| `preference` | Baseado em preferências explícitas e tags         |

As pontuações são ponderadas:

#### `history`

| Fonte             | Peso |
|------------------|------|
| Compras          | 0.4  |
| Carrinho         | 0.3  |
| Navegação        | 0.2  |
| Afinidade        | 0.1  |

#### `preference`

| Fator             | Peso |
|------------------|------|
| Categoria         | 0.4  |
| Tags              | 0.3  |
| Marca             | 0.2  |
| Faixa de preço    | 0.1  |

---

## 🔄 Cache com Redis

- TTL padrão de 72h configurável via `.env`
- Fallback automático se Redis não estiver disponível
- Pode ser limpado via `make reset-cache` ou pelo endpoint:

```http
DELETE /cache
```

---

## 🧪 Testes

```bash
make test
```

> Os testes usam `fakeredis` para não depender de Redis real durante execução.

---

## 📄 Desenvolvimento

Se você quiser rodar manualmente com 3 terminais, rodar apenas o frontend ou testar APIs diretamente:

👉 Veja o [README-dev.md](./README-dev.md)