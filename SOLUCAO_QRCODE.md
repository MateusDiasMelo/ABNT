# 🔧 Solução Completa: QR Code Inválido

## 🔍 Problema Identificado

O backend **NÃO está rodando**, por isso o sistema não consegue gerar QR Codes válidos.

## ✅ Solução Passo a Passo

### 1️⃣ Iniciar o Backend

```bash
cd /home/user/ABNT
./start-backend.sh
```

**O que esse comando faz:**
- Cria ambiente virtual em `backend/venv`
- Instala todas as dependências (incluindo mercadopago e qrcode)
- Inicia servidor FastAPI na porta 8000

**Aguarde ver esta mensagem:**
```
✅ Iniciando servidor FastAPI...
📝 Documentação: http://localhost:8000/api/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2️⃣ Verificar os Logs

Após iniciar o backend, ao criar um pagamento você verá nos logs:

**✅ Se estiver funcionando corretamente:**
```
🔍 Verificando credenciais do Mercado Pago...
   MERCADOPAGO_ACCESS_TOKEN configurado: True
   PAYMENT_DEV_MODE: False
✅ Usando API REAL do Mercado Pago
   Valor: R$ 0.80
   Descrição: Formatação ABNT
🌐 Chamando API do Mercado Pago...
📥 Resposta da API - Status HTTP: 201
✅ Pagamento criado com sucesso!
   Payment ID: 123456789
   Status: pending
   QR Code (string): Presente
   QR Code Base64: Presente
```

**❌ Se estiver usando modo dev (ERRADO):**
```
⚠️  MODO DE DESENVOLVIMENTO - Gerando QR Code FALSO
   Este QR Code NÃO processa pagamentos reais!
```

### 3️⃣ Testar no Frontend

1. Acesse o frontend (geralmente http://localhost:5173)
2. Faça upload de um documento
3. Clique em "Pagar e Baixar"
4. **IMPORTANTE**: Observe os logs do backend no terminal
5. O QR Code gerado deve ser escaneável

### 4️⃣ Se o QR Code Ainda For Inválido

Se você ver nos logs "✅ Usando API REAL" mas o QR Code ainda for inválido, o problema pode ser:

#### A) Credenciais Expiradas ou Inválidas

As credenciais do Mercado Pago podem ter expirado. Para gerar novas:

1. Acesse: https://www.mercadopago.com.br/developers/panel/app
2. Selecione ou crie uma aplicação
3. Vá em "Credenciais"
4. Copie:
   - **Access Token** (começa com APP_USR-...)
   - **Public Key** (começa com APP_USR-...)
5. Atualize em `/home/user/ABNT/backend/.env`:
   ```env
   MERCADOPAGO_ACCESS_TOKEN=APP_USR-novo-token-aqui
   MERCADOPAGO_PUBLIC_KEY=APP_USR-nova-chave-aqui
   ```
6. **REINICIE o backend** (Ctrl+C e ./start-backend.sh novamente)

#### B) Modo de Teste vs Produção

Suas credenciais são de **TESTE** (ambiente sandbox). Para usar:

**Opção 1: Usar App Mercado Pago em Modo Sandbox**
- Crie uma conta de teste em: https://www.mercadopago.com.br/developers/panel/test-accounts
- Use o app do Mercado Pago logado com essa conta de teste

**Opção 2: Usar Credenciais de Produção**
- No painel do Mercado Pago, use "Credenciais de produção" (não "Credenciais de teste")
- Atualize `.env` com as credenciais de produção
- Mude `MERCADOPAGO_TEST_MODE=False`
- Reinicie o backend

#### C) API do Mercado Pago Mudou

Se mesmo com credenciais novas não funcionar, pode haver mudança na API. Verifique:

1. Logs do backend mostram algum erro da API?
2. Status HTTP é 201 ou outro código?
3. `qr_code_base64` está "Presente" ou "AUSENTE"?

Se estiver AUSENTE, a API pode ter mudado e precisaremos ajustar o código.

## 🧪 Script de Diagnóstico

Para verificar status do sistema a qualquer momento:

```bash
cd /home/user/ABNT
./diagnostico.sh
```

Este script mostra:
- ✅ Se .env existe e está configurado
- ✅ Se backend está rodando
- ✅ Se dependências estão instaladas
- ✅ Se configurações estão corretas

## 📋 Checklist de Verificação

- [ ] Backend está rodando? (`./start-backend.sh`)
- [ ] Arquivo `.env` existe em `backend/.env`?
- [ ] `PAYMENT_DEV_MODE=False` no `.env`?
- [ ] Logs mostram "✅ Usando API REAL"?
- [ ] Status HTTP da API é 201?
- [ ] QR Code Base64 está "Presente" nos logs?
- [ ] Credenciais do Mercado Pago são válidas?
- [ ] Conta do Mercado Pago está ativa?

## 🆘 Ainda Não Funciona?

Se seguiu todos os passos e ainda não funciona:

1. **Capture os logs completos** do backend ao gerar pagamento
2. **Tire screenshot** da mensagem de erro do app ao escanear
3. **Verifique** no painel do Mercado Pago se o pagamento foi criado

Possíveis causas raras:
- Conta do Mercado Pago suspensa
- Limite de transações atingido
- Problema de conectividade com API do Mercado Pago
- Mudança na API do Mercado Pago (precisaria atualizar código)

## 📚 Documentação Oficial

- Painel Mercado Pago: https://www.mercadopago.com.br/developers/panel/app
- Documentação PIX: https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-configuration/integrate-with-pix
- Contas de Teste: https://www.mercadopago.com.br/developers/panel/test-accounts

## ✨ Resumo

**O principal problema é que o backend não está rodando.**

Execute:
```bash
cd /home/user/ABNT
./start-backend.sh
```

E observe os logs ao criar um pagamento.
