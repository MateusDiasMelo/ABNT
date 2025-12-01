# ⚙️ Setup Completo - ABNT Formatador

## Pré-requisitos

- Python 3.9+
- Node.js 16+
- Git

## 1. Clone o Repositório

```bash
git clone https://github.com/MateusDiasMelo/ABNT.git
cd ABNT
```

## 2. Configure o Backend

### 2.1. Crie o arquivo .env

```bash
cd backend
cp .env.example .env
```

### 2.2. Edite o .env (opcional)

O arquivo já vem com valores padrão funcionais para desenvolvimento. Se quiser personalizar:

```bash
nano .env  # ou use seu editor favorito
```

**Valores importantes para produção:**
```env
DEBUG=False  # Desativa modo debug
SECRET_KEY=sua-chave-secreta-super-segura
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

**Para habilitar pagamentos:**
```env
MERCADOPAGO_ACCESS_TOKEN=seu-token-mercadopago
STRIPE_SECRET_KEY=sua-chave-stripe
```

### 2.3. Instale as dependências Python

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2.4. Inicie o servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend rodando em: http://localhost:8000

## 3. Configure o Frontend

### 3.1. Instale as dependências

```bash
cd ../frontend  # Se estiver em backend/
npm install
```

### 3.2. Configure variáveis de ambiente (opcional)

```bash
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

### 3.3. Inicie o servidor de desenvolvimento

```bash
npm run dev
```

✅ Frontend rodando em: http://localhost:5173

## 4. Verificação

### Teste o Backend

```bash
curl http://localhost:8000/health
```

Deve retornar:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Teste o Frontend

Abra: http://localhost:5173

Você deve ver a interface do ABNT Formatador.

## 5. Usando Docker (Alternativa)

Se preferir usar Docker:

```bash
# Na raiz do projeto
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

## 6. Estrutura de Diretórios Criada

Após a inicialização, você terá:

```
ABNT/
├── backend/
│   ├── .env                     ✅ Suas configurações
│   ├── venv/                    ✅ Ambiente Python
│   └── abnt.db                  ✅ Banco de dados SQLite
├── uploads/
│   ├── temp/                    ✅ Arquivos enviados
│   └── processed/               ✅ Arquivos processados
└── frontend/
    ├── node_modules/            ✅ Dependências Node
    └── dist/                    ✅ Build de produção (após npm run build)
```

## 7. Configuração de Pagamentos (Opcional)

### Mercado Pago

1. Crie uma conta em: https://www.mercadopago.com.br/developers
2. Obtenha suas credenciais em: Credenciais > Access Token
3. Adicione ao `.env`:
```env
MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890-abcdef
MERCADOPAGO_PUBLIC_KEY=TEST-abcdef-1234567890
```

### Stripe

1. Crie uma conta em: https://dashboard.stripe.com/register
2. Obtenha suas chaves em: Developers > API keys
3. Adicione ao `.env`:
```env
STRIPE_SECRET_KEY=sk_test_1234567890abcdef
STRIPE_PUBLIC_KEY=pk_test_1234567890abcdef
```

## 8. Build para Produção

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Execute com:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run build
```

Os arquivos de produção estarão em `frontend/dist/`.

Sirva com:
```bash
npm run preview
```

## 9. Deploy

### Backend - Opções

- **Railway**: https://railway.app
- **Render**: https://render.com
- **DigitalOcean**: https://www.digitalocean.com
- **AWS EC2**
- **Heroku**

### Frontend - Opções

- **Vercel**: https://vercel.com (Recomendado)
- **Netlify**: https://netlify.com
- **GitHub Pages**
- **Cloudflare Pages**

### Banco de Dados - Opções

- **Supabase** (PostgreSQL): https://supabase.com
- **Render** (PostgreSQL): https://render.com
- **Railway** (PostgreSQL): https://railway.app

## 10. Variáveis de Ambiente para Produção

### Backend (.env)

```env
DEBUG=False
SECRET_KEY=sua-chave-super-secreta-aleatoria-123456789
DATABASE_URL=postgresql://user:pass@host:5432/abnt_prod
ALLOWED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com
MERCADOPAGO_ACCESS_TOKEN=PROD-1234567890
STRIPE_SECRET_KEY=sk_live_1234567890
```

### Frontend (.env)

```env
VITE_API_URL=https://api.seu-dominio.com/api
```

## 11. Comandos Úteis

```bash
# Desenvolvimento rápido
make dev                    # Inicia backend + frontend

# Instalação
make install                # Instala todas as dependências

# Testes
make test                   # Executa testes

# Docker
make docker-up              # Sobe containers
make docker-down            # Derruba containers

# Limpeza
make clean                  # Remove arquivos temporários
make cleanup                # Limpa uploads antigos
```

## 12. Troubleshooting

### Erro: "Module not found"

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "Port already in use"

```bash
# Matar processo na porta 8000
lsof -ti:8000 | xargs kill -9

# Matar processo na porta 5173
lsof -ti:5173 | xargs kill -9
```

### Erro CORS

Verifique se `DEBUG=True` no `.env` do backend.

### Banco de dados não cria

```bash
cd backend
python -c "from app.models.document import Base; from sqlalchemy import create_engine; engine = create_engine('sqlite:///./abnt.db'); Base.metadata.create_all(engine)"
```

## 13. Suporte

- **Documentação**: Veja README.md
- **Issues**: https://github.com/MateusDiasMelo/ABNT/issues
- **API Docs**: http://localhost:8000/api/docs (quando rodando)

---

✅ **Pronto!** Seu ambiente está configurado.

📖 Veja também: [QUICK_START.md](QUICK_START.md) para início rápido.
