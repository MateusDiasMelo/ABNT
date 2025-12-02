# Configuração do MercadoPago

Este guia explica como o MercadoPago está configurado no projeto ABNT Formatador.

## 🎯 Modos de Operação

O sistema suporta dois modos de operação:

### 1. **API Real do MercadoPago (PRIORIDADE)**

Quando as credenciais do MercadoPago estão configuradas, o sistema **SEMPRE** usa a API real, gerando QR Codes PIX válidos e processando pagamentos reais.

```env
MERCADOPAGO_ACCESS_TOKEN=APP_USR-seu-token-aqui
MERCADOPAGO_PUBLIC_KEY=APP_USR-sua-chave-aqui
MERCADOPAGO_TEST_MODE=True  # True para teste, False para produção
```

✅ **QR Code gerado:** PNG real escaneável retornado pela API do MercadoPago
✅ **Formato:** Base64-encoded PNG image
✅ **Documentação:** https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-configuration/integrate-with-pix

### 2. **Modo de Desenvolvimento (FALLBACK)**

Quando as credenciais **NÃO** estão configuradas e `PAYMENT_DEV_MODE=True`, o sistema gera um QR Code falso apenas para testes de interface.

```env
MERCADOPAGO_ACCESS_TOKEN=  # Vazio ou não configurado
PAYMENT_DEV_MODE=True      # Permite fallback para modo dev
```

⚠️ **QR Code gerado:** PNG escaneável mas com dados PIX falsos (não processa pagamento real)
⚠️ **Uso:** Apenas para desenvolvimento local sem credenciais

## 🔑 Credenciais Configuradas

As credenciais do MercadoPago devem estar configuradas no arquivo `.env`:

```env
# Payment Gateways - MercadoPago
MERCADOPAGO_ACCESS_TOKEN=APP_USR-4460565164748962-120120-5a2b81206d26ecaed52dcbbcc7a7e6b8-3033159487
MERCADOPAGO_PUBLIC_KEY=APP_USR-f34a7fe8-92f7-4a15-87ed-603951820dd6
MERCADOPAGO_TEST_MODE=True
```

## 📦 Dependências

A biblioteca do MercadoPago já está incluída no `requirements.txt`:

```
mercadopago==2.2.1
```

## 💳 Funcionalidades Disponíveis

### 1. Criar Pagamento

O serviço de pagamento (`backend/app/services/payment_service.py`) oferece:

```python
from app.services.payment_service import PaymentService

payment_service = PaymentService()

# Criar pagamento via PIX
result = payment_service.create_mercadopago_payment(
    amount=8.00,  # Valor em reais
    description="Formatação ABNT - 10 páginas",
    file_id="arquivo-123",
    payer_email="cliente@example.com"
)

if result["success"]:
    print(f"QR Code PIX: {result['qr_code']}")
    print(f"Payment ID: {result['payment_id']}")
else:
    print(f"Erro: {result['error']}")
```

### 2. Verificar Status do Pagamento

```python
# Verificar se o pagamento foi aprovado
status = payment_service.verify_mercadopago_payment(payment_id)

if status["success"] and status["approved"]:
    print("Pagamento aprovado!")
else:
    print(f"Status: {status['status']}")
```

### 3. Calcular Preço

```python
# Calcular preço baseado no número de páginas
page_count = 10
price = payment_service.calculate_price(page_count)
print(f"Preço: R$ {price:.2f}")  # R$ 8.00 (10 páginas x R$ 0.80)
```

## 🔄 Fluxo de Pagamento

### Passo 1: Upload do Arquivo

```
Cliente faz upload → Sistema processa → Conta páginas
```

### Passo 2: Criação do Pagamento

```python
# No backend após processar o arquivo
payment_result = payment_service.create_mercadopago_payment(
    amount=payment_service.calculate_price(page_count),
    description=f"Formatação ABNT - {file_name}",
    file_id=file_id,
    payer_email=user_email
)
```

### Passo 3: Exibição para Cliente

```
QR Code PIX ← Cliente escaneia e paga
```

### Passo 4: Verificação (Webhook ou Polling)

```python
# Via webhook (recomendado)
@app.post("/api/webhooks/mercadopago")
async def mercadopago_webhook(data: dict):
    payment_id = data.get("data", {}).get("id")
    status = payment_service.verify_mercadopago_payment(payment_id)

    if status["approved"]:
        # Liberar download do arquivo
        # Registrar no Google Sheets
        pass

# Ou via polling (consulta periódica)
while not payment_approved:
    status = payment_service.verify_mercadopago_payment(payment_id)
    if status["approved"]:
        break
    await asyncio.sleep(5)
```

## 🌐 Integração com Google Sheets

Quando um pagamento é criado e aprovado, registre no Google Sheets:

```python
from app.services.sheets_service import SheetsService

sheets_service = SheetsService()

# Ao criar o pagamento
sheets_service.create_payment_record(
    file_id=file_id,
    file_name=file_name,
    page_count=page_count,
    amount=amount,
    payment_method="mercadopago",
    payment_id=payment_result["payment_id"],
    status="pending",
    payer_email=payer_email
)

# Quando o pagamento for aprovado (via webhook)
sheets_service.update_payment_status(
    payment_id=payment_id,
    new_status="approved"
)
```

## 📊 Métodos de Pagamento Suportados

### PIX (Configurado por padrão)

```python
payment_data = {
    "payment_method_id": "pix",
    # ...
}
```

### Cartão de Crédito (opcional)

Para habilitar cartão de crédito, modifique o método `create_mercadopago_payment`:

```python
payment_data = {
    "payment_method_id": "credit_card",
    "token": card_token,  # Token do cartão gerado no frontend
    "installments": 1,
    # ...
}
```

## 🔔 Configurar Webhooks (Recomendado)

### No Painel do MercadoPago

1. Acesse: https://www.mercadopago.com.br/developers/panel
2. Vá em **Webhooks**
3. Configure a URL: `https://seu-dominio.com/api/webhooks/mercadopago`
4. Selecione os eventos:
   - **payment** (payments)

### Endpoint no Backend

```python
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhooks/mercadopago")
async def mercadopago_webhook(request: Request):
    data = await request.json()

    # Validar webhook (recomendado)
    # Processar notificação
    if data.get("type") == "payment":
        payment_id = data.get("data", {}).get("id")

        # Verificar status
        payment_service = PaymentService()
        status = payment_service.verify_mercadopago_payment(payment_id)

        if status["approved"]:
            # Atualizar Google Sheets
            sheets_service = SheetsService()
            sheets_service.update_payment_status(
                payment_id=payment_id,
                new_status="approved"
            )

            # Liberar download, enviar email, etc.

    return {"status": "ok"}
```

## 💰 Configuração de Preços

O preço por página está definido no `.env`:

```env
PRICE_PER_PAGE=0.80
```

Para alterar, modifique este valor e reinicie o servidor.

## 🔒 Segurança

### Credenciais

- ✅ Credenciais já configuradas no `.env`
- ✅ `.env` já está no `.gitignore`
- ⚠️ **NUNCA** commite credenciais no Git

### Validação de Webhooks

É recomendado validar os webhooks do MercadoPago:

```python
import hmac
import hashlib

def validate_webhook(request: Request, secret: str):
    # Obter assinatura do header
    signature = request.headers.get("x-signature")

    # Validar assinatura
    # Ver documentação: https://www.mercadopago.com.br/developers/pt/docs/your-integrations/notifications/webhooks
```

## 📚 Documentação Oficial

- [MercadoPago Developers](https://www.mercadopago.com.br/developers)
- [API Reference](https://www.mercadopago.com.br/developers/pt/reference)
- [SDK Python](https://github.com/mercadopago/sdk-python)

## 🧪 Teste em Sandbox

Para testar pagamentos sem usar dinheiro real:

1. Acesse: https://www.mercadopago.com.br/developers/panel/test-accounts
2. Crie contas de teste
3. Use as credenciais de teste no `.env`
4. Use cartões de teste: https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-test/test-cards

## 🆘 Solução de Problemas

### Erro: "Mercado Pago não configurado"

- Verifique se o `MERCADOPAGO_ACCESS_TOKEN` está definido no `.env`
- Reinicie o servidor após alterar o `.env`

### Pagamento não aprovado

- Para PIX: aguarde o pagamento (pode levar alguns minutos)
- Verifique o status no painel do MercadoPago
- Use `verify_mercadopago_payment()` para consultar o status

### Webhook não recebe notificações

- Certifique-se de que a URL está acessível publicamente
- Use ngrok para testes locais: `ngrok http 8000`
- Configure a URL do ngrok no painel do MercadoPago

## 💡 Próximos Passos

1. ✅ Configurar Google Sheets (veja `GOOGLE_SHEETS_SETUP.md`)
2. 🔄 Implementar webhooks para notificações automáticas
3. 📧 Configurar envio de emails de confirmação
4. 🎨 Criar interface de pagamento no frontend
5. 📊 Implementar dashboard de pagamentos
