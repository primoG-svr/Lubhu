# 🧪 Guia Completo de Testes - Payment Gateway

## 1️⃣ Teste com Docker (Recomendado)

### Passo 1: Inicie os serviços

```bash
cd payment_gateway
docker-compose up -d
```

Aguarde 15-30 segundos para os serviços iniciarem.

**Verifique se tudo está rodando:**
```bash
docker-compose ps
```

Você verá:
- ✅ `payment_gateway_mongodb` - UP
- ✅ `payment_gateway_redis` - UP  
- ✅ `payment_gateway_api` - UP

### Passo 2: Acesse a interface interativa

Abra no navegador:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Passo 3: Health check

```bash
curl http://localhost:8000/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-28T21:35:26.123456Z",
  "environment": "development"
}
```

---

## 2️⃣ Teste Local (Sem Docker)

### Passo 1: Instale dependências

```bash
cd payment_gateway

# Crie ambiente virtual
python -m venv venv

# Ative (Linux/Mac)
source venv/bin/activate
# Ou (Windows)
venv\Scripts\activate

# Instale pacotes
pip install -r requirements.txt
```

### Passo 2: Inicie MongoDB localmente

**Option A - Com Docker (apenas MongoDB):**
```bash
docker run -d -p 27017:27017 --name payment_mongo mongo:5.0
```

**Option B - Instale MongoDB:**
- [Download MongoDB](https://www.mongodb.com/try/download/community)
- Inicie o serviço

### Passo 3: Inicie a API

```bash
python -m uvicorn app.main:app --reload
```

Você verá:
```
Uvicorn running on http://127.0.0.1:8000
```

---

## 3️⃣ Testes com cURL (Terminal)

### 📝 Registrar novo usuário

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "João Silva",
    "password": "Senha@123"
  }'
```

**Resposta esperada (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Salve o `access_token` para próximos comandos:**
```bash
TOKEN="seu_token_aqui"
```

---

### 🔐 Fazer Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Senha@123"
  }'
```

---

### 💳 Registrar Cartão

```bash
curl -X POST "http://localhost:8000/api/v1/cards/register" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366",
    "cardholder_name": "JOAO SILVA",
    "expiry_month": 12,
    "expiry_year": 2026,
    "cvv": "123",
    "is_default": true
  }'
```

**Resposta esperada (201):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "cardholder_name": "JOAO SILVA",
  "last_four": "0366",
  "expiry_month": 12,
  "expiry_year": 2026,
  "card_type": "VISA",
  "is_default": true,
  "is_active": true,
  "created_at": "2026-05-28T21:35:26.123456Z"
}
```

**Salve o `id` do cartão:**
```bash
CARD_ID="507f1f77bcf86cd799439011"
```

---

### ✅ Validar Cartão

```bash
curl -X POST "http://localhost:8000/api/v1/cards/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366",
    "expiry_month": 12,
    "expiry_year": 2026,
    "cvv": "123"
  }'
```

**Resposta esperada (200):**
```json
{
  "is_valid": true,
  "card_type": "VISA",
  "last_four": "0366",
  "message": "Cartão válido"
}
```

---

### 💰 Criar Transação

```bash
curl -X POST "http://localhost:8000/api/v1/transactions/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": "'$CARD_ID'",
    "amount": 150.50,
    "currency": "BRL",
    "description": "Compra na loja online",
    "reference_id": "REF123456789"
  }'
```

**Resposta esperada (201):**
```json
{
  "id": "607f1f77bcf86cd799439012",
  "amount": 150.50,
  "currency": "BRL",
  "status": "completed",
  "description": "Compra na loja online",
  "reference_id": "REF123456789",
  "card_last_four": "0366",
  "fraud_score": 0.0,
  "is_fraud_detected": false,
  "created_at": "2026-05-28T21:35:26.123456Z",
  "completed_at": "2026-05-28T21:35:27.123456Z"
}
```

**Salve o `id` da transação:**
```bash
TRANSACTION_ID="607f1f77bcf86cd799439012"
```

---

### 🔍 Obter Detalhes da Transação

```bash
curl -X GET "http://localhost:8000/api/v1/transactions/$TRANSACTION_ID" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 📋 Listar Todas as Transações

```bash
curl -X GET "http://localhost:8000/api/v1/transactions/?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 💳 Listar Cartões

```bash
curl -X GET "http://localhost:8000/api/v1/cards/list" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 💸 Reembolsar Transação

```bash
curl -X PUT "http://localhost:8000/api/v1/transactions/$TRANSACTION_ID/refund" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Cliente solicitou reembolso",
    "partial_amount": null
  }'
```

---

### 📊 Obter Analytics

```bash
curl -X GET "http://localhost:8000/api/v1/analytics/summary?days=30" \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta esperada:**
```json
{
  "period": "30 days",
  "stats": {
    "total_transactions": 1,
    "total_amount": 150.50,
    "completed_transactions": 1,
    "failed_transactions": 0,
    "pending_transactions": 0,
    "refunded_amount": 150.50,
    "average_transaction_amount": 150.50,
    "fraud_detection_rate": 0.0
  },
  "by_status": {
    "completed": 1,
    "failed": 0,
    "refunded": 1,
    "pending": 0
  },
  "by_currency": {
    "BRL": {
      "count": 1,
      "amount": 150.50
    }
  }
}
```

---

## 4️⃣ Testes Automatizados com Pytest

### Execute todos os testes

```bash
cd payment_gateway

# Instale teste dependencies
pip install pytest pytest-cov

# Execute testes
pytest
```

**Saída esperada:**
```
tests/test_security.py::TestCardValidation::test_valid_card_number_visa PASSED
tests/test_security.py::TestCardValidation::test_invalid_card_number PASSED
tests/test_security.py::TestCardValidation::test_valid_cvv PASSED
tests/test_auth.py::TestAuth::test_register_success PASSED
tests/test_transactions.py::TestTransactions::test_create_transaction_success PASSED

======================== 15 passed in 2.34s ========================
```

### Execute apenas testes de segurança

```bash
pytest tests/test_security.py -v
```

### Execute com cobertura de código

```bash
pytest --cov=app --cov-report=html
```

Abre `htmlcov/index.html` no navegador para ver cobertura detalhada!

---

## 5️⃣ Testes com Postman

### Importe a coleção:

1. Abra [Postman](https://www.postman.com/downloads/)
2. Clique em **File > New**
3. Copie e cole esta coleção:

```json
{
  "info": {
    "name": "Payment Gateway",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/health"
      }
    },
    {
      "name": "Register User",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/auth/register",
        "body": {
          "mode": "raw",
          "raw": "{\"email\": \"user@example.com\", \"full_name\": \"User\", \"password\": \"Pass@123\"}"
        }
      }
    },
    {
      "name": "Register Card",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/cards/register",
        "header": [{"key": "Authorization", "value": "Bearer {{token}}"}],
        "body": {
          "mode": "raw",
          "raw": "{\"card_number\": \"4532015112830366\", \"cardholder_name\": \"USER\", \"expiry_month\": 12, \"expiry_year\": 2026, \"cvv\": \"123\"}"
        }
      }
    },
    {
      "name": "Create Transaction",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/transactions/create",
        "header": [{"key": "Authorization", "value": "Bearer {{token}}"}],
        "body": {
          "mode": "raw",
          "raw": "{\"card_id\": \"{{card_id}}\", \"amount\": 100.00, \"currency\": \"BRL\", \"description\": \"Test\", \"reference_id\": \"REF123\"}"
        }
      }
    }
  ]
}
```

---

## 6️⃣ Cartões de Teste

### Cartões válidos para testar:

| Tipo | Número | CVV | Validade |
|------|--------|-----|----------|
| VISA | 4532015112830366 | 123 | 12/2026 |
| VISA | 4111111111111111 | 123 | 12/2026 |
| MASTERCARD | 5425233010103442 | 123 | 12/2026 |
| AMEX | 378282246310005 | 1234 | 12/2026 |

### Cartões inválidos para testar validação:

```bash
# Número inválido
curl -X POST "http://localhost:8000/api/v1/cards/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "1234567890123456",
    "expiry_month": 12,
    "expiry_year": 2026,
    "cvv": "123"
  }'

# Resposta: is_valid: false, message: "Número de cartão inválido"
```

---

## 7️⃣ Testes de Segurança

### Teste de Senha Fraca

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test",
    "password": "weak"
  }'

# Resposta: 422 Unprocessable Entity
# Senha deve ter: maiúscula, número e caractere especial
```

### Teste de Token Inválido

```bash
curl -X GET "http://localhost:8000/api/v1/cards/list" \
  -H "Authorization: Bearer invalid_token"

# Resposta: 401 Unauthorized
```

### Teste de Acesso não autorizado

```bash
curl -X GET "http://localhost:8000/api/v1/cards/list"

# Resposta: 401 Unauthorized - Token não fornecido
```

---

## 8️⃣ Monitorar Logs

### Logs da API

```bash
docker-compose logs -f api
```

### Logs do MongoDB

```bash
docker-compose logs -f mongodb
```

### Todos os logs

```bash
docker-compose logs -f
```

---

## 9️⃣ Limpar Dados de Teste

### Parar containers

```bash
docker-compose down
```

### Parar e remover volumes (LIMPA TODOS OS DADOS)

```bash
docker-compose down -v
```

### Reiniciar tudo

```bash
docker-compose down -v
docker-compose up -d
```

---

## 🔟 Script de Teste Completo (bash)

Crie arquivo `test_complete.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"

echo "🚀 Iniciando testes completos..."

# 1. Register
echo -e "\n1️⃣ Registrando usuário..."
REGISTER=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test'$(date +%s)'@example.com",
    "full_name": "Test User",
    "password": "TestPass@123"
  }')

TOKEN=$(echo $REGISTER | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo "✅ Token: ${TOKEN:0:50}..."

# 2. Register Card
echo -e "\n2️⃣ Registrando cartão..."
CARD=$(curl -s -X POST "$BASE_URL/cards/register" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366",
    "cardholder_name": "TEST USER",
    "expiry_month": 12,
    "expiry_year": 2026,
    "cvv": "123"
  }')

CARD_ID=$(echo $CARD | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "✅ Card ID: $CARD_ID"

# 3. Create Transaction
echo -e "\n3️⃣ Criando transação..."
TRANSACTION=$(curl -s -X POST "$BASE_URL/transactions/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": "'$CARD_ID'",
    "amount": 99.99,
    "currency": "BRL",
    "description": "Test Transaction",
    "reference_id": "REF'$(date +%s)'"
  }')

TRANSACTION_ID=$(echo $TRANSACTION | grep -o '"id":"[^"]*' | cut -d'"' -f4 | head -1)
echo "✅ Transaction ID: $TRANSACTION_ID"

# 4. Get Analytics
echo -e "\n4️⃣ Obtendo analytics..."
curl -s -X GET "$BASE_URL/analytics/summary?days=30" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool

echo -e "\n\n✅ Testes completos!"
```

Execute:
```bash
chmod +x test_complete.sh
./test_complete.sh
```

---

## 🎯 Checklist de Testes

- [ ] Health check retorna status healthy
- [ ] Registro de usuário com sucesso
- [ ] Login funciona
- [ ] Registro de cartão funciona
- [ ] Validação de cartão funciona
- [ ] Criação de transação funciona
- [ ] Listagem de transações funciona
- [ ] Reembolso de transação funciona
- [ ] Analytics retorna dados
- [ ] Teste de senha fraca é rejeitado
- [ ] Token inválido é rejeitado
- [ ] Testes automatizados passam (pytest)
- [ ] Cobertura de código >80%

---

## 📞 Troubleshooting

### API não inicia
```bash
# Verifique se porta 8000 está em uso
lsof -i :8000
# Se sim, mate o processo
kill -9 <PID>
```

### MongoDB não conecta
```bash
# Verifique se MongoDB está rodando
docker-compose logs mongodb

# Reinicie
docker-compose restart mongodb
```

### Erro de token inválido
```bash
# Gere um novo token fazendo login novamente
# O token expira em 30 minutos
```

### Testes falhando
```bash
# Limpe dados antigos
docker-compose down -v
docker-compose up -d

# Aguarde 30 segundos e tente novamente
sleep 30
pytest
```

---

Divirta-se testando! 🎉
