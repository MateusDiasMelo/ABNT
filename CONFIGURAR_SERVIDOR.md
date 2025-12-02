# 🚀 Como Configurar Credenciais no Servidor Hospedado

## ✅ Erro Atual (Esperado)

```
Erro: Credenciais do Mercado Pago não configuradas no servidor.
Contate o administrador do sistema.
```

**Isso está CORRETO!** O sistema detectou que não há credenciais no servidor e está avisando ao invés de gerar QR Code falso.

---

## 🎯 Solução: Adicionar Credenciais no Servidor

Dependendo de como seu servidor está configurado, escolha a opção abaixo:

---

## 📋 OPÇÃO 1: Servidor com Acesso SSH (Mais Comum)

### Passo 1: Conecte ao servidor via SSH

```bash
ssh usuario@seu-servidor.com
# Ou se usar chave:
ssh -i sua-chave.pem usuario@seu-servidor.com
```

### Passo 2: Navegue até o diretório do backend

```bash
cd /caminho/para/seu/projeto/backend
# Exemplo comum:
cd /var/www/abnt/backend
# Ou:
cd /home/usuario/abnt/backend
```

### Passo 3: Crie/edite o arquivo .env

```bash
# Use nano (mais fácil para iniciantes):
nano .env

# Ou vim:
vim .env

# Ou vi:
vi .env
```

### Passo 4: Adicione suas credenciais

Cole estas linhas no arquivo:

```env
# Application
APP_NAME=ABNT Formatador
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=seu-secret-key-de-producao-aqui

# Server
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com

# Database
DATABASE_URL=sqlite:///./abnt.db

# Redis
REDIS_URL=redis://localhost:6379/0

# Payment Gateway (PIX via MercadoPago)
# SUAS CREDENCIAIS REAIS DO MERCADO PAGO
MERCADOPAGO_ACCESS_TOKEN=APP_USR-4460565164748962-120120-5a2b81206d26ecaed52dcbbcc7a7e6b8-3033159487
MERCADOPAGO_PUBLIC_KEY=APP_USR-f34a7fe8-92f7-4a15-87ed-603951820dd6
MERCADOPAGO_TEST_MODE=True

# Google Sheets Database
GOOGLE_SHEETS_SPREADSHEET_ID=
GOOGLE_SHEETS_CREDENTIALS_FILE=google_credentials.json

# Pricing
PRICE_PER_PAGE=0.80

# File Upload
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=docx,pdf
UPLOAD_DIR=uploads/temp
PROCESSED_DIR=uploads/processed

# File Cleanup
FILE_RETENTION_HOURS=24

# ABNT Settings
DEFAULT_FONT=Times New Roman
DEFAULT_FONT_SIZE=12
DEFAULT_LINE_SPACING=1.5
```

### Passo 5: Salve o arquivo

**Se usar nano:**
- `Ctrl + O` (salvar)
- `Enter` (confirmar)
- `Ctrl + X` (sair)

**Se usar vim/vi:**
- `ESC` (modo comando)
- `:wq` (salvar e sair)
- `Enter`

### Passo 6: Reinicie o backend

```bash
# Opção 1: Se usar systemctl
sudo systemctl restart abnt-backend
# Verifique status:
sudo systemctl status abnt-backend

# Opção 2: Se usar PM2
pm2 restart abnt-backend
# Verifique logs:
pm2 logs abnt-backend

# Opção 3: Se usar Docker
docker-compose restart backend
# Verifique logs:
docker-compose logs -f backend

# Opção 4: Se rodar diretamente
pkill -f uvicorn
cd /caminho/para/backend
./start-backend.sh
# Ou:
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Passo 7: Verifique os logs

```bash
# Se usar systemctl:
sudo journalctl -u abnt-backend -f

# Se usar PM2:
pm2 logs abnt-backend --lines 50

# Se usar Docker:
docker-compose logs -f backend

# Se rodar direto:
# Os logs aparecem no terminal
```

**PROCURE por estas linhas nos logs:**
```
============================================================
🔍 VERIFICAÇÃO DE CREDENCIAIS DO MERCADO PAGO
============================================================
📋 MERCADOPAGO_ACCESS_TOKEN configurado: True  ← DEVE SER True
```

---

## 🐳 OPÇÃO 2: Servidor com Docker

### Método A: Arquivo .env montado

**1. Crie .env no servidor:**
```bash
ssh usuario@servidor
cd /caminho/para/projeto
nano backend/.env
# Cole as credenciais (mesmo conteúdo acima)
```

**2. Garanta que docker-compose.yml monta o .env:**
```yaml
services:
  backend:
    volumes:
      - ./backend:/app
      - ./backend/.env:/app/.env  # Adicione esta linha se não existir
```

**3. Reinicie:**
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f backend
```

### Método B: Variáveis de ambiente no Docker

**1. Edite docker-compose.yml no servidor:**
```bash
nano docker-compose.yml
```

**2. Adicione as variáveis:**
```yaml
services:
  backend:
    environment:
      - MERCADOPAGO_ACCESS_TOKEN=APP_USR-4460565164748962-120120-5a2b81206d26ecaed52dcbbcc7a7e6b8-3033159487
      - MERCADOPAGO_PUBLIC_KEY=APP_USR-f34a7fe8-92f7-4a15-87ed-603951820dd6
      - MERCADOPAGO_TEST_MODE=True
      - DEBUG=False
```

**3. Reinicie:**
```bash
docker-compose down
docker-compose up -d
```

---

## ☁️ OPÇÃO 3: Plataformas de Hospedagem (Heroku, Render, Railway, etc)

### Heroku

```bash
# Via CLI:
heroku config:set MERCADOPAGO_ACCESS_TOKEN=APP_USR-4460565164748962-120120-5a2b81206d26ecaed52dcbbcc7a7e6b8-3033159487
heroku config:set MERCADOPAGO_PUBLIC_KEY=APP_USR-f34a7fe8-92f7-4a15-87ed-603951820dd6
heroku config:set MERCADOPAGO_TEST_MODE=True
```

**Ou via painel:**
1. Acesse dashboard do Heroku
2. Vá em Settings → Config Vars
3. Adicione as variáveis

### Render

1. Acesse dashboard do Render
2. Selecione seu serviço
3. Vá em Environment
4. Adicione as variáveis:
   - `MERCADOPAGO_ACCESS_TOKEN`
   - `MERCADOPAGO_PUBLIC_KEY`
   - `MERCADOPAGO_TEST_MODE`

### Railway

1. Acesse dashboard do Railway
2. Selecione seu projeto
3. Vá em Variables
4. Adicione as variáveis

### Vercel/Netlify (Se backend separado)

1. Acesse dashboard
2. Settings → Environment Variables
3. Adicione as variáveis

---

## 🔍 Como Verificar Se Funcionou

### 1. Via Logs (Recomendado)

Após reiniciar, crie um pagamento no site e observe os logs.

**✅ SUCESSO - Deve aparecer:**
```
============================================================
🔍 VERIFICAÇÃO DE CREDENCIAIS DO MERCADO PAGO
============================================================
📋 MERCADOPAGO_ACCESS_TOKEN configurado: True
📋 Token (primeiros 30 chars): APP_USR-4460565164748962-1201...
============================================================
✅ USANDO API REAL DO MERCADO PAGO
============================================================
```

**❌ AINDA COM ERRO - Aparece:**
```
📋 MERCADOPAGO_ACCESS_TOKEN configurado: False
```

Se ainda False, o backend não está lendo as variáveis. Veja troubleshooting abaixo.

### 2. Via Site

1. Acesse seu site hospedado
2. Faça upload de um documento
3. Clique em "Pagar e Baixar"
4. **Resultado esperado:**
   - ✅ QR Code válido aparece
   - ❌ Se ainda erro, verifique logs

---

## 🆘 Troubleshooting

### Problema: Ainda mostra "Credenciais não configuradas"

**Causa 1: .env não está no lugar certo**
```bash
# Verifique se existe:
ls -la /caminho/para/backend/.env

# Deve aparecer o arquivo. Se não:
# Você criou no lugar errado
```

**Causa 2: Backend não reiniciou**
```bash
# Mate TODOS os processos:
ps aux | grep uvicorn
# Anote os PIDs e mate:
kill -9 PID_DO_PROCESSO

# Reinicie
```

**Causa 3: Backend não está lendo .env**
```bash
# Teste se Python consegue ler:
cd /caminho/para/backend
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('MERCADOPAGO_ACCESS_TOKEN'))"

# Deve mostrar seu token. Se mostrar None:
# O .env não está sendo lido
```

**Causa 4: Permissões do arquivo**
```bash
# Dê permissão de leitura:
chmod 644 /caminho/para/backend/.env
```

**Causa 5: Docker não monta .env**
```bash
# Verifique se .env está dentro do container:
docker exec -it nome_do_container ls -la /app/.env

# Se não existir, ajuste docker-compose.yml
```

### Problema: QR Code aparece mas é inválido

**Causa: Credenciais expiradas**
1. Acesse: https://www.mercadopago.com.br/developers/panel/app
2. Gere novas credenciais
3. Atualize no .env
4. Reinicie

### Problema: Não consigo acessar o servidor SSH

**Solução:**
1. Entre em contato com sua hospedagem
2. Peça acesso SSH ou painel de variáveis de ambiente
3. Ou peça para eles configurarem as variáveis

---

## 📝 Checklist Final

Após configurar, verifique:

- [ ] Arquivo .env existe no servidor em `/caminho/para/backend/.env`
- [ ] MERCADOPAGO_ACCESS_TOKEN tem valor real (não exemplo)
- [ ] MERCADOPAGO_PUBLIC_KEY tem valor real (não exemplo)
- [ ] Backend foi reiniciado após criar .env
- [ ] Logs mostram "✅ USANDO API REAL DO MERCADO PAGO"
- [ ] Logs mostram "📋 MERCADOPAGO_ACCESS_TOKEN configurado: True"
- [ ] QR Code aparece no site
- [ ] QR Code é escaneável e válido

---

## 🔐 Segurança

- ✅ .env está no .gitignore (não vai para Git)
- ✅ Use credenciais de TESTE para testar
- ✅ Use credenciais de PRODUÇÃO para produção
- ⚠️ NUNCA commite credenciais no Git
- ⚠️ Em produção, use DEBUG=False

---

## 💡 Dica Rápida

**Não sabe onde está o backend no servidor?**
```bash
# Procure:
find / -name "app" -type d 2>/dev/null | grep abnt

# Ou:
ps aux | grep uvicorn
# Veja o caminho do processo
```

---

## 📞 Precisa de Ajuda?

Se ainda não funcionar:

1. **Capture os logs completos** ao criar pagamento
2. **Verifique** se .env foi criado: `cat /caminho/para/backend/.env`
3. **Verifique** se backend reiniciou: `ps aux | grep uvicorn`
4. **Compartilhe** os logs (sem expor credenciais completas)

Os logs vão mostrar exatamente qual é o problema!
