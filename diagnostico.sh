#!/bin/bash

echo "==================================="
echo "🔍 Diagnóstico do Sistema de Pagamentos"
echo "==================================="
echo ""

cd /home/user/ABNT/backend

echo "1️⃣ Verificando arquivo .env..."
if [ -f ".env" ]; then
    echo "   ✅ Arquivo .env encontrado"
    echo "   📋 Conteúdo (credenciais mascaradas):"
    echo ""
    grep "MERCADOPAGO_ACCESS_TOKEN" .env | sed 's/\(APP_USR-[^-]*-[^-]*-\).*/\1.../'
    grep "PAYMENT_DEV_MODE" .env
    echo ""
else
    echo "   ❌ Arquivo .env NÃO encontrado!"
    echo ""
fi

echo "2️⃣ Verificando backend..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo "   ✅ Backend está RODANDO na porta 8000"
else
    echo "   ❌ Backend NÃO está rodando!"
    echo "   💡 Execute: ./start-backend.sh"
fi
echo ""

echo "3️⃣ Verificando dependências..."
if [ -d "venv" ]; then
    echo "   ✅ Ambiente virtual encontrado"
    source venv/bin/activate
    if python -c "import mercadopago" 2>/dev/null; then
        echo "   ✅ mercadopago instalado"
    else
        echo "   ❌ mercadopago NÃO instalado"
    fi
    if python -c "import qrcode" 2>/dev/null; then
        echo "   ✅ qrcode instalado"
    else
        echo "   ❌ qrcode NÃO instalado"
    fi
    deactivate
else
    echo "   ❌ Ambiente virtual NÃO encontrado"
    echo "   💡 Execute: ./start-backend.sh"
fi
echo ""

echo "4️⃣ Teste de configuração (se venv existir)..."
if [ -d "venv" ]; then
    source venv/bin/activate
    python3 << 'EOF'
try:
    from app.core.config import get_settings
    s = get_settings()
    print(f"   MERCADOPAGO_ACCESS_TOKEN configurado: {bool(s.MERCADOPAGO_ACCESS_TOKEN)}")
    print(f"   PAYMENT_DEV_MODE: {s.PAYMENT_DEV_MODE}")
    if s.MERCADOPAGO_ACCESS_TOKEN:
        print(f"   TOKEN (primeiros 20): {s.MERCADOPAGO_ACCESS_TOKEN[:20]}...")
    else:
        print("   ⚠️  TOKEN VAZIO!")
except Exception as e:
    print(f"   ❌ Erro ao carregar configurações: {e}")
EOF
    deactivate
fi
echo ""

echo "==================================="
echo "💡 Próximos Passos:"
echo "==================================="
echo ""
echo "Se backend NÃO está rodando:"
echo "   cd /home/user/ABNT"
echo "   ./start-backend.sh"
echo ""
echo "Se backend está rodando mas QR Code inválido:"
echo "   1. Verifique se .env existe com credenciais corretas"
echo "   2. Reinicie o backend (Ctrl+C e ./start-backend.sh novamente)"
echo "   3. Verifique os logs ao gerar pagamento"
echo ""
echo "Se ainda não funcionar:"
echo "   - Credenciais podem ter expirado"
echo "   - Gere novas em: https://www.mercadopago.com.br/developers/panel/app"
echo ""
