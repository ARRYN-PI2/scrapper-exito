# Makefile para el proyecto Scraper Éxito

.PHONY: help install test lint format run clean docker-build docker-run

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
	python -m venv venv
	venv/bin/pip install -r requirements.txt
	venv/bin/playwright install

test: ## Ejecutar pruebas
	venv/bin/pytest tests/ -v --cov=src

lint: ## Ejecutar linter
	venv/bin/flake8 src/ tests/
	venv/bin/mypy src/

format: ## Formatear código
	venv/bin/black src/ tests/
	venv/bin/isort src/ tests/

run-manual: ## Ejecutar scraper manualmente
	venv/bin/python -m src.interfaces.cli.main

run-scheduler: ## Ejecutar scheduler
	venv/bin/python -m src.infrastructure.schedulers.scheduler

clean: ## Limpiar archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/

docker-build: ## Construir imagen Docker
	docker-compose build

docker-run: ## Ejecutar con Docker
	docker-compose up -d

docker-stop: ## Detener contenedores Docker
	docker-compose down

docker-logs: ## Ver logs de Docker
	docker-compose logs -f scraper

init-git: ## Inicializar repositorio Git
	git init
	git add .
	git commit -m "Initial commit: Project structure created"

setup: install init-git ## Configuración inicial completa
	@echo "¡Proyecto configurado exitosamente!"
