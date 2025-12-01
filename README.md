# ABNT Formatador Automático

Aplicativo web para formatação automática de trabalhos acadêmicos seguindo as normas ABNT (NBR 14724 e NBR 6023).

## 🎯 Funcionalidades

- ✅ Upload de arquivos DOCX e PDF
- ✅ Formatação automática ABNT NBR 14724
- ✅ Formatação de referências NBR 6023
- ✅ Contagem automática de páginas
- ✅ Sistema de cobrança (R$ 0,80/página)
- ✅ Integração com gateway de pagamento
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

## 🚀 Instalação

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## 🔧 Configuração

1. Copie o arquivo `.env.example` para `.env`
2. Configure as variáveis de ambiente:
   - `DATABASE_URL`: URL do banco de dados
   - `MERCADOPAGO_ACCESS_TOKEN`: Token do Mercado Pago
   - `SECRET_KEY`: Chave secreta para JWT

## 💻 Execução

### Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
```

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
