# 🚀 Payment Gateway - Setup Completo

## ⚡ Quick Start (Recomendado)

### Windows
```bash
cd payment_gateway
start.bat
```

### Linux / macOS
```bash
cd payment_gateway
bash start.sh
```

---

## 📋 Pré-requisitos

- ✅ **Docker** e **Docker Compose** instalados
- ✅ **Node.js 18+** e **npm** instalados
- ✅ **Python 3.10+** (opcional, se rodar sem Docker)
- ✅ Portas disponíveis: 3000, 8000, 27017, 6379

### Verificar instalação

```bash
# Docker
docker --version
docker-compose --version

# Node.js
node --version
npm --version

# Python (opcional)
python --version
```

---

## 🔧 Setup Manual

### Backend (Terminal 1)

```bash
cd payment_gateway

# Iniciar Docker
docker-compose up -d

# Aguarde 15-30 segundos

# Verificar se está rodando
docker-compose ps

# Ver logs
docker-compose logs -f api
```

**Backend rodando em:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- MongoDB: localhost:27017
- Redis: localhost:6379

### Frontend (Terminal 2)

```bash
cd payment_gateway/frontend

# Instalar dependências (primeira vez)
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

**Frontend rodando em:**
- http://localhost:3000

---

## 🌐 Acessar a Aplicação

### Frontend
- **Home:** http://localhost:3000
- **Login:** http://localhost:3000/login
- **Dashboard:** http://localhost:3000/dashboard

### Backend
- **API:** http://localhost:8000
- **Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health:** http://localhost:8000/health

---

## 📝 Contas de Teste

### Registrar novo usuário
1. Acesse http://localhost:3000/register
2. Preencha os dados:
   - Email: seu@email.com
   - Nome: Seu Nome
   - Senha: Senha@123
3. Clique em "Criar Conta"

### Cartões de teste

| Tipo | Número | CVV | Validade |
|------|--------|-----|----------|
| VISA | 4532015112830366 | 123 | 12/2026 |
| MASTERCARD | 5425233010103442 | 123 | 12/2026 |
| AMEX | 378282246310005 | 1234 | 12/2026 |

---

## 🧪 Testes Automatizados

### Rodar testes unitários

```bash
cd payment_gateway
pytest tests/test_security.py -v
```

### Rodar todos os testes

```bash
cd payment_gateway
pytest --cov=app --cov-report=html
```

### Abrir relatório de cobertura

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## 🛠️ Comandos Úteis

### Docker

```bash
cd payment_gateway

# Iniciar
docker-compose up -d

# Parar
docker-compose down

# Parar e remover volumes (limpa dados)
docker-compose down -v

# Ver logs
docker-compose logs -f api

# Reiniciar
docker-compose restart

# Status
docker-compose ps
```

### Frontend

```bash
cd payment_gateway/frontend

# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Iniciar build
npm start

# Linting
npm run lint

# Limpar cache
rm -rf .next node_modules
npm install
```

---

## 🔒 Variáveis de Ambiente

### Backend (.env)

```bash
cd payment_gateway
cp .env.example .env
```

Edite se necessário:
```
DATABASE_URL=mongodb://localhost:27017/payment_gateway
SECRET_KEY=your_super_secret_key_change_in_production
ENCRYPTION_KEY=your_encryption_key_32_chars
```

### Frontend (.env.local)

```bash
cd payment_gateway/frontend
cp .env.example .env.local
```

Edite se necessário:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
```

---

## 🐛 Troubleshooting

### Porta 3000 já em uso

```bash
# Mude a porta
cd payment_gateway/frontend
npm run dev -- -p 3001

# Acesse: http://localhost:3001
```

### Porta 8000 já em uso

```bash
# Mude a porta no backend
cd payment_gateway
uvicorn app.main:app --port 8001

# Atualize .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Docker não inicia

```bash
# Verifique permissões
sudo usermod -aG docker $USER

# Reinicie Docker
sudo systemctl restart docker

# Tente novamente
docker-compose up -d
```

### Node modules não encontrado

```bash
cd payment_gateway/frontend
rm -rf node_modules
npm install
npm run dev
```

### Erro de conexão com API

```bash
# Verifique se backend está rodando
curl http://localhost:8000/health

# Se não responder, inicie backend
cd payment_gateway
docker-compose up -d
```

---

## 📊 Fluxo Completo de Teste

1. **Registrar** → http://localhost:3000/register
2. **Fazer login** → http://localhost:3000/login
3. **Adicionar cartão** → http://localhost:3000/cards
4. **Fazer transação** → http://localhost:3000/checkout
5. **Ver histórico** → http://localhost:3000/transactions
6. **Analytics** → http://localhost:3000/dashboard

---

## 📚 Documentação

- [API Documentation](http://localhost:8000/docs)
- [Testing Guide](./TESTING.md)
- [Backend README](./README.md)

---

## 📞 Suporte

Para issues e dúvidas:
- Abra uma issue no GitHub
- Verifique os logs: `docker-compose logs -f`
- Teste manualmente com cURL: `curl http://localhost:8000/health`

---

**Happy coding! 🚀**