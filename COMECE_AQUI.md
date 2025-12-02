# ⚠️ PROBLEMA: QR Code Inválido

## 🎯 CAUSA RAIZ IDENTIFICADA

**Seu backend NÃO está rodando!**

Por isso o sistema não consegue gerar QR Codes válidos do Mercado Pago.

---

## ✅ SOLUÇÃO (3 passos simples)

### Passo 1: Inicie o Backend

Abra um terminal e execute:

```bash
cd /home/user/ABNT
./start-backend.sh
```

**Aguarde aparecer:**
```
✅ Iniciando servidor FastAPI...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Passo 2: Teste no Frontend

1. Acesse http://localhost:5173 (ou sua porta do frontend)
2. Faça upload de um documento
3. Clique em "Pagar e Baixar"
4. **OBSERVE OS LOGS DO BACKEND** no terminal

### Passo 3: Verifique os Logs

**✅ DEVE aparecer isto (correto):**
```
🔍 Verificando credenciais do Mercado Pago...
   MERCADOPAGO_ACCESS_TOKEN configurado: True
   PAYMENT_DEV_MODE: False
✅ Usando API REAL do Mercado Pago
   Valor: R$ 0.80
🌐 Chamando API do Mercado Pago...
📥 Resposta da API - Status HTTP: 201
✅ Pagamento criado com sucesso!
   QR Code Base64: Presente
```

**❌ Se aparecer isto (errado):**
```
⚠️  MODO DE DESENVOLVIMENTO - Gerando QR Code FALSO
```

Significa que o .env não está sendo lido. Reinicie o backend.

---

## 🔍 Se Ainda Não Funcionar

### Diagnóstico Rápido

```bash
cd /home/user/ABNT
./diagnostico.sh
```

### Possíveis Causas

1. **Credenciais Expiradas** (mais provável)
   - Suas credenciais do Mercado Pago podem ter expirado
   - Gere novas em: https://www.mercadopago.com.br/developers/panel/app
   - Atualize em `/home/user/ABNT/backend/.env`
   - Reinicie o backend

2. **Modo de Teste**
   - Suas credenciais são de TESTE (sandbox)
   - Para testar, use conta de teste do Mercado Pago
   - Ou use credenciais de produção

3. **API Mudou**
   - Se logs mostram "QR Code Base64: AUSENTE"
   - A API do Mercado Pago pode ter mudado
   - Precisaria atualizar o código

---

## 📋 Status Atual (via diagnóstico)

```
✅ Arquivo .env configurado com suas credenciais
✅ PAYMENT_DEV_MODE=False (vai usar API real quando backend iniciar)
❌ Backend NÃO está rodando
❌ Ambiente virtual não existe ainda
```

**SOLUÇÃO:** Execute `./start-backend.sh`

---

## 📚 Guia Completo

Para troubleshooting detalhado, veja:
- `SOLUCAO_QRCODE.md` - Guia completo passo a passo
- `INSTRUCOES_TESTE.md` - Instruções de teste
- `diagnostico.sh` - Script de verificação

---

## 💡 TL;DR

```bash
# Passo 1: Inicie o backend
cd /home/user/ABNT
./start-backend.sh

# Passo 2: Acesse o frontend e teste
# http://localhost:5173

# Passo 3: Observe os logs do backend
# Deve mostrar "✅ Usando API REAL do Mercado Pago"
```

Se mesmo assim não funcionar, as credenciais do Mercado Pago provavelmente expiraram.
