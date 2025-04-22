# Subir todos os serviços
up:
	docker-compose up --build

# Derrubar tudo
down:
	docker-compose down

# Ver logs de todos os serviços
logs:
	docker-compose logs -f

# Build manual
build:
	docker-compose build

# Reiniciar apenas o frontend
restart-frontend:
	docker-compose restart frontend

# Entrar no container da API principal
shell-api:
	docker exec -it llm_api /bin/bash

# Entrar no container da BFF
shell-bff:
	docker exec -it bff_api /bin/bash

# Rodar testes da API principal
test:
	docker exec -it llm_api pytest --disable-warnings

# Limpar cache Redis (se tiver rota configurada)
reset-cache:
	curl -X DELETE http://localhost:8000/cache || true