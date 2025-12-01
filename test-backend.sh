#!/bin/bash

echo "🧪 Testando Backend ABNT Formatador..."

# Testa endpoint raiz
echo -e "\n1. Testando endpoint raiz (/)..."
curl -s http://localhost:8000/ | python3 -m json.tool

# Testa health check
echo -e "\n2. Testando health check (/health)..."
curl -s http://localhost:8000/health | python3 -m json.tool

# Testa CORS
echo -e "\n3. Testando CORS..."
curl -s -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/api/upload \
     -I

echo -e "\n✅ Testes básicos concluídos!"
