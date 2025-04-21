# Recommender System with LLM (Mock)

Este projeto é uma solução para um desafio técnico que envolve:

- Sistema de recomendação baseado em histórico de compras
- Integração com IA Generativa via simulador LLM
- API RESTful com FastAPI
- Arquitetura seguindo princípios SOLID
- Fallback automático para descrição genérica

## Como rodar

1. Instale as dependências:
```
pip install -r requirements.txt
```

2. Inicie o servidor:
```
uvicorn main:app --reload
```

3. Acesse a documentação em: `http://localhost:8000/docs`
