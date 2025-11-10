.PHONY: help install test run docker-build docker-run deploy

help:
	@echo "Comandos disponíveis:"
	@echo "  install     - Instala dependências"
	@echo "  test        - Executa testes"
	@echo "  run         - Executa localmente"
	@echo "  docker-build- Constrói imagem Docker"
	@echo "  docker-run  - Executa container Docker"
	@echo "  deploy      - Faz deploy no GCP"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

run:
	uvicorn app.main:app --reload --port 8080

docker-build:
	docker build -t finalprojectftl .

docker-run:
	docker run -p 8080:8080 --env-file .env finalprojectftl

deploy:
	./scripts/deploy.sh