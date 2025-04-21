
# Recommender System with LLM (Mock)

Este projeto é uma solução para um desafio técnico que envolve:

- Sistema de recomendação baseado em histórico de comportamento do usuário
- Integração com IA Generativa via simulador LLM
- API RESTful com FastAPI
- Arquitetura modular seguindo princípios SOLID
- Estratégias intercambiáveis com uso do padrão Strategy
- Fallback automático para descrições genéricas

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

---

## ✅ Sobre os testes

Este projeto segue uma abordagem rigorosa para a implementação dos testes unitários. As regras adotadas são:

- Cada pasta do projeto possui uma pasta de testes correspondente (`tests/`)
- Cada arquivo de código possui uma pasta homônima dentro de `tests/`
- Cada classe do código testado possui um arquivo `.py` próprio para seus testes
- Cada método da classe testada possui uma **classe `TestX` específica**
- Cada teste segue a estrutura **AAA (Arrange, Act, Assert)**
- Os nomes dos testes seguem a convenção:  
  `test_if_<condicao>_should_<comportamento>` ou `test_should_<comportamento>`
- **Não é permitido o uso de lógica condicional ou estruturas de controle (if, for, while, etc)** nos testes
- Linhas com mais de 79 caracteres recebem `# noqa`

Essa padronização facilita a leitura, a rastreabilidade dos testes e garante cobertura próxima de 100%.

---

## 🧠 Estratégias de recomendação para usuários

O sistema de recomendação permite múltiplas estratégias que podem ser trocadas dinamicamente. Atualmente, usamos duas implementações principais:

### 1. `HistoryBasedRecommendationStrategy`

Esta estratégia avalia o comportamento do usuário com base em ações passadas. A pontuação de recomendação é calculada com base em quatro fatores:

| Fonte                 | Peso no score |
|----------------------|---------------|
| `purchase_history`   | 0.4           |
| `cart_events`        | 0.3           |
| `browsing_history`   | 0.2           |
| `match with preferences` | 0.1     |

Cada produto é avaliado e recebe pontos por cada evidência de interesse. O score final é **limitado a 1.0** e um campo `reason` descritivo é gerado com base nos fatores que contribuíram.

### 2. `PreferenceBasedRecommendationStrategy`

Essa estratégia foca nas **preferências explícitas** do usuário, considerando:

- Categorias favoritas
- Marcas preferidas
- Tags compatíveis
- Produtos dentro da **faixa de preço observada no histórico de compras**

A pontuação também é normalizada com pesos:

| Fator                      | Peso |
|---------------------------|------|
| Categoria preferida       | 0.4  |
| Tags compatíveis          | 0.3  |
| Marca preferida           | 0.2  |
| Preço dentro da faixa     | 0.1  |

Todos os produtos do catálogo são avaliados e ordenados pela nota final. Produtos que se alinham com múltiplas preferências são priorizados.

---

Este README foi estruturado para explicar o funcionamento técnico do projeto, ajudar na execução local e orientar sobre as decisões de design e testes.
