#!/bin/bash

echo "🚀 Iniciando ABNT Formatador Backend..."

cd backend

# Verifica se o virtualenv existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa virtualenv
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo "📥 Instalando dependências..."
pip install --quiet -r requirements.txt

# Cria diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p ../uploads/temp ../uploads/processed

# Inicia servidor
echo "✅ Iniciando servidor FastAPI..."
echo "📝 Documentação: http://localhost:8000/api/docs"
echo ""
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
