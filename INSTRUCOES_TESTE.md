# 🔧 Instruções para Testar QR Code do Mercado Pago

## ✅ Correções Aplicadas

1. **Arquivo `.env` criado** com suas credenciais reais do Mercado Pago
2. **`PAYMENT_DEV_MODE=False`** para forçar uso da API real
3. **Logs detalhados** adicionados para debugging

## 🚀 Como Testar

### 1. Reinicie o Backend

O backend precisa ser reiniciado para carregar as novas configurações do arquivo `.env`:

```bash
cd /home/user/ABNT/backend

# Mate o processo atual (se estiver rodando)
pkill -f uvicorn

# Inicie novamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Verifique os Logs

Ao criar um pagamento, você verá logs detalhados no terminal do backend:

```
🔍 Verificando credenciais do Mercado Pago...
   MERCADOPAGO_ACCESS_TOKEN configurado: True
   PAYMENT_DEV_MODE: False
✅ Usando API REAL do Mercado Pago
   Valor: R$ 8.00
   Descrição: Formatação ABNT - 10 páginas
🌐 Chamando API do Mercado Pago...
📥 Resposta da API - Status HTTP: 201
✅ Pagamento criado com sucesso!
   Payment ID: 123456789
   Status: pending
   QR Code (string): Presente
   QR Code Base64: Presente
   QR Code Base64 length: 12345
```

### 3. O que Verificar

- ✅ Logs devem mostrar "Usando API REAL do Mercado Pago"
- ✅ Status HTTP deve ser 201
- ✅ QR Code Base64 deve estar "Presente"
- ✅ QR Code deve ser escaneável pelo app do seu banco
- ✅ QR Code deve pertencer à sua conta do Mercado Pago

### 4. Se Ainda Aparecer "QR Code não é mais válido"

Isso pode significar:

1. **Credenciais incorretas**: Verifique se as credenciais em `/home/user/ABNT/backend/.env` estão corretas
2. **Modo de teste**: As credenciais são de teste? Use o app do Mercado Pago em modo sandbox
3. **Token expirado**: Gere novas credenciais no painel do Mercado Pago

## 🔍 Credenciais Configuradas

Arquivo: `/home/user/ABNT/backend/.env`

```env
MERCADOPAGO_ACCESS_TOKEN=APP_USR-4460565164748962-120120-5a2b81206d26ecaed52dcbbcc7a7e6b8-3033159487
MERCADOPAGO_PUBLIC_KEY=APP_USR-f34a7fe8-92f7-4a15-87ed-603951820dd6
MERCADOPAGO_TEST_MODE=True
PAYMENT_DEV_MODE=False  ← IMPORTANTE: False para usar API real
```

## 📝 Logs de Debugging

Os logs agora mostram:

- ✅ Se está usando API real ou modo dev
- ✅ Status da chamada à API
- ✅ Se o QR Code foi retornado corretamente
- ✅ Tamanho do QR Code Base64
- ⚠️ Avisos se algo estiver errado

## 🆘 Troubleshooting

### Problema: Logs ainda mostram "MODO DE DESENVOLVIMENTO"

**Solução**: Verifique se o arquivo `.env` foi criado em `/home/user/ABNT/backend/.env`

```bash
cat /home/user/ABNT/backend/.env | grep PAYMENT_DEV_MODE
# Deve mostrar: PAYMENT_DEV_MODE=False
```

### Problema: "Credenciais do Mercado Pago NÃO configuradas"

**Solução**: O arquivo `.env` não está sendo lido. Reinicie o servidor:

```bash
cd /home/user/ABNT/backend
pkill -f uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Problema: QR Code ainda inválido mesmo com API real

**Possíveis causas**:

1. **Credenciais de teste sem conta sandbox**: Se `MERCADOPAGO_TEST_MODE=True`, você precisa de uma conta de teste no Mercado Pago
2. **Token inválido**: As credenciais podem ter expirado. Gere novas em: https://www.mercadopago.com.br/developers/panel/app
3. **Conta suspensa**: Verifique se sua conta do Mercado Pago está ativa

## 📚 Documentação Mercado Pago

- Painel de credenciais: https://www.mercadopago.com.br/developers/panel/app
- Documentação PIX: https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-configuration/integrate-with-pix
- Contas de teste: https://www.mercadopago.com.br/developers/panel/test-accounts
