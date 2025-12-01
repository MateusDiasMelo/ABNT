.PHONY: help install dev build test clean docker-up docker-down

help:
	@echo "ABNT Formatador - Comandos Disponíveis"
	@echo ""
	@echo "  make install       - Instala dependências (backend + frontend)"
	@echo "  make dev          - Inicia desenvolvimento local"
	@echo "  make build        - Build de produção"
	@echo "  make test         - Executa testes"
	@echo "  make clean        - Limpa arquivos temporários"
	@echo "  make docker-up    - Inicia com Docker Compose"
	@echo "  make docker-down  - Para containers Docker"
	@echo "  make cleanup      - Executa limpeza de arquivos"

install:
	@echo "Instalando dependências do backend..."
	cd backend && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Instalando dependências do frontend..."
	cd frontend && npm install
	@echo "✅ Instalação concluída!"

dev:
	@echo "Iniciando servidores de desenvolvimento..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@make -j2 dev-backend dev-frontend

dev-backend:
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

build:
	@echo "Building para produção..."
	cd frontend && npm run build
	@echo "✅ Build concluído!"

test:
	@echo "Executando testes do backend..."
	cd backend && . venv/bin/activate && pytest
	@echo "Executando testes do frontend..."
	cd frontend && npm test
	@echo "✅ Testes concluídos!"

clean:
	@echo "Limpando arquivos temporários..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	rm -rf uploads/temp/* uploads/processed/*
	@echo "✅ Limpeza concluída!"

docker-up:
	@echo "Iniciando containers Docker..."
	docker-compose up -d
	@echo "✅ Containers iniciados!"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "Docs: http://localhost:8000/api/docs"

docker-down:
	@echo "Parando containers Docker..."
	docker-compose down
	@echo "✅ Containers parados!"

cleanup:
	@echo "Executando limpeza de arquivos antigos..."
	cd backend && python -m app.utils.file_cleanup
	@echo "✅ Limpeza concluída!"
