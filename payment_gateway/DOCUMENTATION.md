# 📋 Documentação Completa - Payment Gateway

## 📑 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Instalação](#instalação)
4. [Uso](#uso)
5. [API Reference](#api-reference)
6. [Frontend](#frontend)
7. [Segurança](#segurança)
8. [Performance](#performance)
9. [Deploy](#deploy)

---

## Visão Geral

### O Que É?
Payment Gateway é uma solução completa para processar pagamentos de forma segura com:
- Autenticação JWT
- Criptografia AES-256
- Validação de cartões
- Analytics em tempo real
- Interface web moderna

### Arquitetura
```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│              http://localhost:3000                       │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/JSON
┌────────────────────────▼────────────────────────────────┐
│                    Backend (FastAPI)                     │
│              http://localhost:8000                       │
├─────────────────────────────────────────────────────────┤
│  • Autenticação JWT                                      │
│  • Validação de cartões                                  │
│  • Processamento de transações                           │
│  • Analytics e relatórios                                │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  Banco de Dados                          │
├─────────────────────────────────────────────────────────┤
│  • MongoDB (27017) - Dados principais                    │
│  • Redis (6379) - Cache e rate limiting                  │
└─────────────────────────────────────────────────────────┘
```

---

## Instalação

### Requisitos Mínimos
- Docker e Docker Compose
- Node.js 18+
- npm ou yarn

### Passo 1: Clonar e Entrar no Diretório
```bash
cd payment_gateway
```

### Passo 2: Iniciar Backend
```bash
docker-compose up -d
```

Verifique se está rodando:
```bash
docker-compose ps
```

### Passo 3: Iniciar Frontend
```bash
cd frontend
npm install
npm run dev
```

### Passo 4: Verificar
```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

---

## Uso

### Registrar Novo Usuário

**Frontend:**
1. Acesse http://localhost:3000/register
2. Preencha dados
3. Clique "Criar Conta"

**API:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "Password@123"
  }'
```

### Fazer Login

**Frontend:**
1. Acesse http://localhost:3000/login
2. Preencha email e senha
3. Clique "Entrar"

**API:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password@123"
  }'
```

### Adicionar Cartão

**Frontend:**
1. Acesse http://localhost:3000/cards
2. Clique "Novo Cartão"
3. Preencha dados
4. Clique "Salvar"

**API:**
```bash
TOKEN="seu_token_aqui"

curl -X POST http://localhost:8000/api/v1/cards/register \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366",
    "cardholder_name": "JOHN DOE",
    "expiry_month": 12,
    "expiry_year": 2026,
    "cvv": "123"
  }'
```

### Processar Transação

**Frontend:**
1. Acesse http://localhost:3000/checkout
2. Selecione cartão
3. Preencha valor
4. Clique "Realizar Pagamento"

**API:**
```bash
curl -X POST http://localhost:8000/api/v1/transactions/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": "card_id_aqui",
    "amount": 150.50,
    "currency": "BRL",
    "description": "Compra na loja",
    "reference_id": "REF123456"
  }'
```

---

## API Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Headers Requeridos
```
Authorization: Bearer {token}
Content-Type: application/json
```

### Endpoints

#### POST /auth/register
**Registrar novo usuário**

Request:
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "Password@123"
}
```

Response (201):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### POST /auth/login
**Fazer login**

Request:
```json
{
  "email": "user@example.com",
  "password": "Password@123"
}
```

Response (200):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### POST /cards/register
**Registrar novo cartão**

Request:
```json
{
  "card_number": "4532015112830366",
  "cardholder_name": "JOHN DOE",
  "expiry_month": 12,
  "expiry_year": 2026,
  "cvv": "123",
  "is_default": true
}
```

Response (201):
```json
{
  "id": "507f1f77bcf86cd799439011",
  "cardholder_name": "JOHN DOE",
  "last_four": "0366",
  "expiry_month": 12,
  "expiry_year": 2026,
  "card_type": "VISA",
  "is_default": true,
  "is_active": true,
  "created_at": "2026-05-28T21:35:26.123456Z"
}
```

#### POST /transactions/create
**Criar transação**

Request:
```json
{
  "card_id": "507f1f77bcf86cd799439011",
  "amount": 150.50,
  "currency": "BRL",
  "description": "Compra na loja",
  "reference_id": "REF123456789"
}
```

Response (201):
```json
{
  "id": "607f1f77bcf86cd799439012",
  "amount": 150.50,
  "currency": "BRL",
  "status": "completed",
  "description": "Compra na loja",
  "reference_id": "REF123456789",
  "card_last_four": "0366",
  "fraud_score": 0.0,
  "is_fraud_detected": false,
  "created_at": "2026-05-28T21:35:26.123456Z",
  "completed_at": "2026-05-28T21:35:27.123456Z"
}
```

#### GET /transactions
**Listar transações**

Parameters:
```
skip=0&limit=10&status=completed
```

Response (200):
```json
{
  "total": 1,
  "page": 1,
  "per_page": 10,
  "transactions": [...]
}
```

#### GET /analytics/summary
**Obter estatísticas**

Parameters:
```
days=30
```

Response (200):
```json
{
  "period": "30 days",
  "stats": {
    "total_transactions": 10,
    "total_amount": 1500.50,
    "completed_transactions": 9,
    "failed_transactions": 1,
    "pending_transactions": 0,
    "refunded_amount": 0.00,
    "average_transaction_amount": 150.05,
    "fraud_detection_rate": 0.0
  },
  "by_status": {...},
  "by_currency": {...}
}
```

---

## Frontend

### Páginas

#### Home (/)
- Hero section
- Features
- Call to action

#### Login (/login)
- Formulário de login
- Link para registro

#### Register (/register)
- Formulário de registro
- Validação de senha
- Link para login

#### Dashboard (/dashboard)
- Estatísticas em cards
- Ações rápidas
- Status de transações

#### Checkout (/checkout)
- Seleção de cartão
- Entrada de valor
- Descrição da transação

#### Cards (/cards)
- Listagem de cartões
- Formulário de novo cartão
- Cartão padrão destacado

#### Transactions (/transactions)
- Listagem com filtros
- Detalhes expandíveis
- Botão de reembolso

### Componentes

#### Navbar
```tsx
<Navbar />
```
Barra de navegação com links e logout

#### Button
```tsx
<Button variant="primary" disabled={isLoading}>
  Clique aqui
</Button>
```
Botão com variantes: primary, secondary, danger

#### Card
```tsx
<Card title="Título">
  Conteúdo
</Card>
```
Container com título opcional

---

## Segurança

### Autenticação
- JWT com expiração de 30 minutos
- Refresh token com expiração de 7 dias
- Hash bcrypt para senhas
- Validação de senha forte

### Criptografia
- AES-256 para cartões
- AES-256 para CVV
- HTTPS ready (em produção)

### Validação
- Algoritmo de Luhn para cartões
- Validação de CVV (3-4 dígitos)
- Validação de expiração
- Email validation
- Rate limiting (100 req/min)

### Proteção
- CORS configurado
- Trusted Host middleware
- CSRF protection ready
- SQL/NoSQL injection prevention
- Audit logs

---

## Performance

### Otimizações Backend
- Índices MongoDB
- Cache Redis
- Rate limiting
- Connection pooling

### Otimizações Frontend
- Code splitting
- Image optimization
- Lazy loading
- Minification

---

## Deploy

### Preparação
1. Atualize variáveis de ambiente
2. Configure HTTPS
3. Mude SECRET_KEY e ENCRYPTION_KEY
4. Desabilite DEBUG

### Opções de Deploy

#### AWS EC2
```bash
# 1. SSH na instância
ssh -i key.pem ubuntu@ip

# 2. Clone repositório
git clone seu_repo
cd payment_gateway

# 3. Inicie com Docker
docker-compose up -d
```

#### Heroku
```bash
# 1. Instale Heroku CLI
# 2. Login
heroku login

# 3. Crie app
heroku create seu_app

# 4. Configure variáveis
heroku config:set SECRET_KEY=...

# 5. Deploy
git push heroku main
```

#### DigitalOcean
```bash
# 1. SSH na droplet
ssh root@ip

# 2. Instale Docker
curl -fsSL https://get.docker.com -o get-docker.sh | sh

# 3. Clone e inicie
git clone seu_repo
cd payment_gateway
docker-compose up -d
```

---

**Documentação completa pronta para uso! 🎉**
