@echo off
REM Ativar o ambiente virtual no backend
cd backend
call venv\Scripts\activate

REM Instalar o Uvicorn (caso não tenha sido instalado ainda)
pip install uvicorn

REM Rodar o backend (Uvicorn)
start cmd /K "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Voltar para o diretório do frontend
cd ..\frontend

REM Rodar o frontend (Vite)
start cmd /K "npm run dev"
