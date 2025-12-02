# 🚨 IMPORTANTE: QR Code Genérico REMOVIDO

## ⚠️ O Que Mudou

**ANTES:**
- Sistema tinha modo "desenvolvimento" que gerava QR Code genérico/falso
- Se credenciais não configuradas → gerava QR Code inválido
- Confuso saber se estava usando API real ou não

**AGORA:**
- Sistema **SEMPRE** usa API real do Mercado Pago
- Sem credenciais válidas → **ERRO CLARO** (nunca gera QR Code falso)
- Logs detalhados mostram exatamente o que está acontecendo

---

## 🔍 Por Que Estava Gerando QR Code Genérico no Servidor

O servidor em produção está gerando QR Code genérico porque:

### Opção 1: Arquivo `.env` não existe no servidor
```bash
# O servidor não tem este arquivo:
/caminho/para/backend/.env
```

### Opção 2: Credenciais inválidas no `.env`
```bash
# O .env tem valores de exemplo:
MERCADOPAGO_ACCESS_TOKEN=APP_USR-your-access-token-here
```

### Opção 3: Variáveis de ambiente não configuradas
Se usar Docker/serviço, as variáveis podem não estar sendo passadas.

---

## ✅ SOLUÇÃO: Configure Credenciais no Servidor

### Passo 1: Crie/Edite o arquivo `.env` no servidor

```bash
# No servidor, crie o arquivo:
nano /caminho/para/backend/.env

# Ou edite se já existir:
vim /caminho/para/backend/.env
```

### Passo 2: Adicione suas credenciais REAIS

```env
# Payment Gateway (PIX via MercadoPago)
# IMPORTANT: System ALWAYS uses real MercadoPago API
MERCADOPAGO_ACCESS_TOKEN=APP_USR-4460565164748962-120120-5a2b81206d26ecaed52dcbbcc7a7e6b8-3033159487
MERCADOPAGO_PUBLIC_KEY=APP_USR-f34a7fe8-92f7-4a15-87ed-603951820dd6
MERCADOPAGO_TEST_MODE=True
```

### Passo 3: Reinicie o backend no servidor

```bash
# Mate o processo atual
pkill -f uvicorn

# Ou se usar systemctl:
sudo systemctl restart abnt-backend

# Ou se usar docker:
docker-compose restart backend

# Ou se usar pm2:
pm2 restart abnt-backend
```

---

## 🧪 Como Verificar Se Funciona

### 1. Monitore os Logs do Servidor

Ao criar um pagamento, você DEVE ver nos logs:

**✅ SUCESSO (credenciais corretas):**
```
============================================================
🔍 VERIFICAÇÃO DE CREDENCIAIS DO MERCADO PAGO
============================================================
📋 MERCADOPAGO_ACCESS_TOKEN configurado: True
📋 Token (primeiros 30 chars): APP_USR-4460565164748962-1201...
============================================================
✅ USANDO API REAL DO MERCADO PAGO
============================================================
💰 Valor: R$ 0.80
📝 Descrição: Formatação ABNT
============================================================
🌐 Chamando API do Mercado Pago...
============================================================
📥 RESPOSTA DA API DO MERCADO PAGO
============================================================
📊 Status HTTP: 201
✅ Payment ID: 123456789
✅ Status: pending
============================================================
🔍 ANÁLISE DO QR CODE RETORNADO
============================================================
📱 QR Code (string PIX): ✅ PRESENTE
🖼️  QR Code Base64 (imagem): ✅ PRESENTE
📏 Tamanho do Base64: 12345 caracteres
✅ QR Code válido retornado pela API do Mercado Pago
============================================================
```

**❌ ERRO (sem credenciais):**
```
============================================================
🔍 VERIFICAÇÃO DE CREDENCIAIS DO MERCADO PAGO
============================================================
📋 MERCADOPAGO_ACCESS_TOKEN configurado: False
============================================================
╔════════════════════════════════════════════════════════════╗
║  ❌ ERRO: CREDENCIAIS DO MERCADO PAGO NÃO CONFIGURADAS    ║
╚════════════════════════════════════════════════════════════╝

MOTIVO: O servidor NÃO tem credenciais válidas do Mercado Pago.
```

### 2. Teste no Frontend

1. Acesse o site em produção
2. Faça upload de um documento
3. Clique em "Pagar e Baixar"
4. **Observe o comportamento:**
   - ✅ QR Code real do Mercado Pago aparece
   - ❌ Mensagem de erro clara aparece
   - ❌ Nunca mais aparece QR Code genérico

---

## 📋 Checklist de Configuração no Servidor

- [ ] Arquivo `.env` existe em `/caminho/para/backend/.env`
- [ ] `MERCADOPAGO_ACCESS_TOKEN` está com valor real (não exemplo)
- [ ] `MERCADOPAGO_PUBLIC_KEY` está com valor real (não exemplo)
- [ ] Backend foi reiniciado após criar/editar `.env`
- [ ] Logs mostram "✅ USANDO API REAL DO MERCADO PAGO"
- [ ] QR Code gerado é escaneável e válido
- [ ] Nunca mais aparece QR Code genérico

---

## 🐳 Se Usar Docker

### Opção 1: Arquivo `.env` montado como volume

```yaml
# docker-compose.yml
services:
  backend:
    volumes:
      - ./backend/.env:/app/.env  # Monta o .env
```

### Opção 2: Variáveis de ambiente diretas

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - MERCADOPAGO_ACCESS_TOKEN=APP_USR-seu-token-aqui
      - MERCADOPAGO_PUBLIC_KEY=APP_USR-sua-chave-aqui
      - MERCADOPAGO_TEST_MODE=True
```

---

## 🔒 Segurança

- ✅ `.env` está no `.gitignore` (não é commitado)
- ✅ Credenciais ficam apenas no servidor
- ⚠️ **NUNCA** commite credenciais no Git
- ⚠️ Use credenciais de TESTE para desenvolvimento
- ⚠️ Use credenciais de PRODUÇÃO para produção

---

## 🆘 Troubleshooting

### "Credenciais não configuradas" mesmo com .env

**Causa:** Backend não está lendo o arquivo .env

**Solução:**
1. Verifique caminho do .env (deve estar em `/backend/.env`)
2. Verifique permissões: `chmod 644 /caminho/para/backend/.env`
3. Reinicie o backend completamente

### QR Code ainda genérico após configurar

**Causa:** Código antigo ainda em execução

**Solução:**
1. Faça pull do código atualizado: `git pull origin nome-do-branch`
2. Mate TODOS os processos do backend: `pkill -9 -f uvicorn`
3. Reinicie: `./start-backend.sh`

### Status HTTP não é 201

**Causa:** Credenciais inválidas ou expiradas

**Solução:**
1. Gere novas credenciais em: https://www.mercadopago.com.br/developers/panel/app
2. Atualize o .env
3. Reinicie o backend

---

## 📚 Documentação

- Painel Mercado Pago: https://www.mercadopago.com.br/developers/panel/app
- Documentação PIX: https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-configuration/integrate-with-pix
- Credenciais de Teste: https://www.mercadopago.com.br/developers/panel/test-accounts

---

## ✨ Resumo

1. **Sistema agora NUNCA gera QR Code genérico**
2. **Sempre exige credenciais reais do Mercado Pago**
3. **Logs detalhados mostram exatamente o que está acontecendo**
4. **Configure `.env` no servidor com credenciais reais**
5. **Reinicie o backend após configurar**
6. **Monitore os logs para confirmar sucesso**
