# ABNT Formatador Automático

Aplicativo web para formatação automática de trabalhos acadêmicos seguindo as normas ABNT (NBR 14724 e NBR 6023).

## 🎯 Funcionalidades

- ✅ Upload de arquivos DOCX e PDF
- ✅ Formatação automática ABNT NBR 14724
- ✅ Formatação de referências NBR 6023
- ✅ Contagem automática de páginas
- ✅ Sistema de cobrança (R$ 0,80/página)
- ✅ Integração com gateway de pagamento (PIX)
- ✅ QR Code PIX com código para copiar e colar
- ✅ Envio automático por email após pagamento
- ✅ Download do arquivo formatado

## 📋 Requisitos

### Backend
- Python 3.9+
- FastAPI
- python-docx
- PyPDF2
- reportlab

### Frontend
- Node.js 16+
- React 18+
- TypeScript
- Vite

## 🚀 Início Rápido

### Método 1: Script Automático (Recomendado)

```bash
# Terminal 1 - Backend
./start-backend.sh

# Terminal 2 - Frontend
cd frontend
npm install && npm run dev
```

Acesse: **http://localhost:5173**

### Método 2: Docker

```bash
docker-compose up -d
```

### Método 3: Manual

Veja o guia completo: **[SETUP.md](SETUP.md)**

## 📚 Documentação

- **[QUICK_START.md](QUICK_START.md)** - Início rápido (5 minutos)
- **[SETUP.md](SETUP.md)** - Configuração completa e detalhada
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Como contribuir
- **API Docs** - http://localhost:8000/api/docs (após iniciar backend)

## ⚠️ Solução de Problemas

### ❌ Erro CORS (mais comum)

Se você ver este erro no console do navegador:
```
Requisição cross-origin bloqueada: A diretiva Same Origin não permite a leitura...
```

**Solução:**

1. Certifique-se que o arquivo `backend/.env` existe:
```bash
cd backend
cp .env.example .env
```

2. Verifique que `DEBUG=True` no arquivo `.env`

3. Reinicie o backend:
```bash
./start-backend.sh
```

### ❌ Erro "Module not found"

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ Porta em uso

```bash
# Backend (porta 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (porta 5173)
lsof -ti:5173 | xargs kill -9
```

## 🔧 Configuração de Pagamentos (Opcional)

O aplicativo funciona sem configurar pagamentos (para testes).

Para habilitar pagamentos reais, edite `backend/.env`:

```env
# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu-token-aqui
MERCADOPAGO_PUBLIC_KEY=sua-chave-publica

# Stripe
STRIPE_SECRET_KEY=sua-chave-secreta
STRIPE_PUBLIC_KEY=sua-chave-publica
```

## 📧 Configuração de Email (Opcional)

O aplicativo pode enviar automaticamente o documento formatado por email após a confirmação do pagamento.

Para habilitar o envio de emails, edite `backend/.env`:

```env
# Email Settings (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-de-app
SMTP_FROM_EMAIL=noreply@abntformatador.com
SMTP_FROM_NAME=ABNT Formatador
SMTP_USE_TLS=True
```

**Nota para Gmail:**
- Use uma "Senha de App" em vez da senha da conta
- Gere em: https://myaccount.google.com/apppasswords
- Ative a verificação em duas etapas primeiro

## 📐 Regras ABNT Implementadas

### NBR 14724 - Formatação

- **Papel**: A4 (21cm x 29,7cm)
- **Margens**: Superior/Esquerda: 3cm; Inferior/Direita: 2cm
- **Fonte**: Times New Roman ou Arial, tamanho 12
- **Espaçamento**: 1,5 para texto, simples para citações e referências
- **Parágrafo**: Recuo de 1,25cm
- **Alinhamento**: Justificado
- **Numeração**: Arábica, canto superior direito

### NBR 6023 - Referências

- Alinhamento à esquerda
- Espaçamento simples
- Separação por espaço simples em branco

## 💰 Sistema de Cobrança

- **Preço**: R$ 0,80 por página final formatada
- **Pagamento**: Via Mercado Pago ou Stripe
- **Download**: Liberado após confirmação do pagamento

## 🔒 Segurança

- Arquivos temporários excluídos após 24 horas
- Upload com validação de tipo e tamanho
- Autenticação JWT para downloads

## 📝 Estrutura do Projeto

```
ABNT/
├── backend/
│   ├── app/
│   │   ├── api/          # Rotas da API
│   │   ├── core/         # Configurações
│   │   ├── services/     # Lógica de negócio
│   │   ├── models/       # Modelos de dados
│   │   └── utils/        # Utilitários
│   ├── tests/            # Testes
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   ├── pages/        # Páginas
│   │   ├── services/     # Serviços API
│   │   └── utils/        # Utilitários
│   └── package.json
└── uploads/              # Arquivos temporários
```

## 🧪 Testes

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 📄 Licença

MIT

## 👥 Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.
