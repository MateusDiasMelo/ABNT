# 🚀 Guia Rápido de Inicialização

## Início Rápido (5 minutos)

### 1. Backend (Terminal 1)

```bash
cd ABNT
./start-backend.sh
```

Aguarde até ver:
```
✅ Iniciando servidor FastAPI...
📝 Documentação: http://localhost:8000/api/docs
```

### 2. Frontend (Terminal 2)

```bash
cd ABNT/frontend
npm install
npm run dev
```

Aguarde até ver:
```
➜  Local:   http://localhost:5173/
```

### 3. Acesse o Aplicativo

Abra seu navegador em: **http://localhost:5173**

## Testes Rápidos

### Testar Backend

```bash
cd ABNT
./test-backend.sh
```

### Testar Upload (com curl)

```bash
# Criar arquivo de teste
echo "Teste ABNT" > test.txt

# Fazer upload
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test.txt" \
  -H "Content-Type: multipart/form-data"
```

## Solução de Problemas

### Erro CORS

Se ver erro de CORS no console:

1. Verifique se o backend está rodando: `curl http://localhost:8000/health`
2. Verifique se DEBUG=True no arquivo `backend/.env`
3. Reinicie o backend

### Erro de Módulo Python

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Porta em Uso

**Backend (8000)**:
```bash
lsof -ti:8000 | xargs kill -9
```

**Frontend (5173)**:
```bash
lsof -ti:5173 | xargs kill -9
```

## Estrutura de Arquivos Criados

```
ABNT/
├── backend/
│   ├── .env                    ✅ Configurações
│   ├── venv/                   ✅ Ambiente Python (criado ao iniciar)
│   └── abnt.db                 ✅ Banco SQLite (criado automaticamente)
├── uploads/
│   ├── temp/                   ✅ Arquivos temporários
│   └── processed/              ✅ Arquivos processados
└── frontend/
    └── node_modules/           ✅ Dependências (criado com npm install)
```

## URLs Importantes

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/api/docs
- **Redoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

## Próximos Passos

1. **Testar Upload**: Arraste um arquivo DOCX ou PDF na interface
2. **Ver Processamento**: Aguarde a formatação ABNT
3. **Configurar Pagamento** (opcional):
   - Edite `backend/.env`
   - Adicione tokens do Mercado Pago ou Stripe

## Desenvolvimento

### Hot Reload Ativo

Ambos frontend e backend têm **hot reload** ativo:
- Mudanças no código Python recarregam automaticamente
- Mudanças no código React recarregam automaticamente

### Adicionar Nova Rota (Backend)

Edite: `backend/app/api/routes.py`

### Adicionar Novo Componente (Frontend)

Crie em: `frontend/src/components/NomeComponente.tsx`

## Logs

### Backend
Os logs aparecem no terminal onde você executou `./start-backend.sh`

### Frontend
Os logs aparecem:
- Terminal: onde você executou `npm run dev`
- Browser: Console do desenvolvedor (F12)

## Parar os Servidores

- **Ctrl+C** em cada terminal
- Ou use `make docker-down` se estiver usando Docker
