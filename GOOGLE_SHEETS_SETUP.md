# Configuração do Google Sheets como Banco de Dados

Este guia explica como configurar o Google Sheets para funcionar como banco de dados do projeto ABNT Formatador.

## 📋 Pré-requisitos

- Conta Google
- Planilha do Google Sheets criada (já configurada: `14xdDMRAfea5xBwpfahxbOLOcb_W5TaTE0f11iv3J0pE`)

## 🔑 Passo 1: Criar Service Account no Google Cloud

### 1.1. Acessar Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Faça login com sua conta Google
3. Crie um novo projeto ou selecione um existente

### 1.2. Habilitar APIs Necessárias

1. No menu lateral, vá em **APIs & Services** > **Library**
2. Procure e habilite as seguintes APIs:
   - **Google Sheets API**
   - **Google Drive API**

### 1.3. Criar Service Account

1. No menu lateral, vá em **APIs & Services** > **Credentials**
2. Clique em **Create Credentials** > **Service Account**
3. Preencha os dados:
   - **Service account name**: `abnt-formatador-sheets`
   - **Service account description**: `Acesso ao Google Sheets para ABNT Formatador`
4. Clique em **Create and Continue**
5. Em **Grant this service account access to project**, selecione a role **Editor**
6. Clique em **Continue** e depois **Done**

### 1.4. Gerar Chave JSON

1. Na lista de Service Accounts, clique na conta recém-criada
2. Vá na aba **Keys**
3. Clique em **Add Key** > **Create new key**
4. Selecione **JSON** como tipo
5. Clique em **Create**
6. O arquivo JSON será baixado automaticamente

### 1.5. Configurar a Chave no Projeto

1. Renomeie o arquivo baixado para `google_credentials.json`
2. Mova o arquivo para o diretório `backend/` do projeto:
   ```bash
   mv ~/Downloads/nome-do-arquivo.json backend/google_credentials.json
   ```

## 📝 Passo 2: Compartilhar a Planilha

### 2.1. Obter o Email da Service Account

1. Abra o arquivo `google_credentials.json`
2. Copie o valor do campo `client_email`
   - Deve ser algo como: `abnt-formatador-sheets@nome-projeto.iam.gserviceaccount.com`

### 2.2. Compartilhar a Planilha

1. Abra a planilha no Google Sheets:
   - https://docs.google.com/spreadsheets/d/14xdDMRAfea5xBwpfahxbOLOcb_W5TaTE0f11iv3J0pE
2. Clique no botão **Compartilhar** (canto superior direito)
3. Cole o email da service account
4. Defina a permissão como **Editor**
5. **IMPORTANTE**: Desmarque a opção "Notificar pessoas"
6. Clique em **Compartilhar**

## ⚙️ Passo 3: Configurar Variáveis de Ambiente

O arquivo `.env` já está configurado com:

```env
# Google Sheets Database
GOOGLE_SHEETS_SPREADSHEET_ID=14xdDMRAfea5xBwpfahxbOLOcb_W5TaTE0f11iv3J0pE
GOOGLE_SHEETS_CREDENTIALS_FILE=google_credentials.json
```

## 🚀 Passo 4: Instalar Dependências e Configurar

### 4.1. Instalar Dependências Python

```bash
cd backend
pip install -r requirements.txt
```

### 4.2. Executar Script de Setup

```bash
python setup_sheets.py
```

Este script irá:
- Conectar ao Google Sheets
- Criar as abas necessárias (Pagamentos e Arquivos)
- Configurar os cabeçalhos das planilhas

## 📊 Estrutura das Planilhas

### Aba: Pagamentos

| Data/Hora | ID Arquivo | Nome Arquivo | Páginas | Valor | Método | ID Pagamento | Status | Email |
|-----------|------------|--------------|---------|-------|--------|--------------|--------|-------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Aba: Arquivos

| Data/Hora | ID Arquivo | Nome | Caminho Original | Caminho Processado | Páginas | Status |
|-----------|------------|------|------------------|-------------------|---------|--------|
| ... | ... | ... | ... | ... | ... | ... |

## 🔒 Segurança

### Arquivos que NÃO devem ir para o Git

O `.gitignore` já está configurado para ignorar:
- `backend/.env` - Variáveis de ambiente com credenciais
- `backend/google_credentials.json` - Credenciais do Google Cloud

### ⚠️ IMPORTANTE

**NUNCA** commite os seguintes arquivos:
- `google_credentials.json`
- `.env`

Estes arquivos contêm informações sensíveis e devem ser mantidos localmente.

## 🧪 Testando a Integração

### Teste Rápido com Python

```python
from app.services.sheets_service import SheetsService

# Inicializa o serviço
sheets = SheetsService()

# Cria um registro de teste
sheets.create_payment_record(
    file_id="test-123",
    file_name="documento.docx",
    page_count=10,
    amount=8.00,
    payment_method="mercadopago",
    payment_id="mp-123456",
    status="approved",
    payer_email="teste@example.com"
)

print("✓ Registro criado com sucesso!")
```

## 🆘 Solução de Problemas

### Erro: "Arquivo de credenciais não encontrado"

- Verifique se o arquivo `google_credentials.json` está no diretório `backend/`
- Confirme que o nome do arquivo está correto

### Erro: "Permission denied" ou "403"

- Certifique-se de que compartilhou a planilha com o email da service account
- Verifique se a permissão é de **Editor**

### Erro: "API not enabled"

- Volte ao Google Cloud Console
- Habilite as APIs: Google Sheets API e Google Drive API

### Erro ao conectar

- Verifique se o `GOOGLE_SHEETS_SPREADSHEET_ID` no `.env` está correto
- Confirme que as credenciais JSON estão válidas

## 📚 Referências

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [gspread Documentation](https://docs.gspread.org/)
- [Google Cloud Service Accounts](https://cloud.google.com/iam/docs/service-accounts)

## 💡 Dicas

1. **Backup**: Faça backup periódico da planilha
2. **Permissões**: Mantenha o acesso à planilha restrito
3. **Monitoramento**: Acompanhe o uso da API no Google Cloud Console
4. **Limites**: A API do Google Sheets tem limites de uso. Para produção, considere implementar cache
