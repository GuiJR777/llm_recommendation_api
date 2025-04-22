FROM python:3.10-slim

WORKDIR /app

# Copia o requirements.txt da raiz do projeto
COPY ../../requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia os arquivos da API BFF (relativo ao contexto passado no docker-compose)
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001", "--reload"]
