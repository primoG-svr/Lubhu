import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Database
from bson import ObjectId

client = TestClient(app)

class TestTransactions:
    """Testes de transações"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        Database.connect()
        db = Database.get_db()
        
        # Limpar dados
        db.users.delete_many({})
        db.cards.delete_many({})
        db.transactions.delete_many({})
        
        # Criar usuário de teste
        user = db.users.insert_one({
            "email": "test@example.com",
            "full_name": "Test User",
            "hashed_password": "hashed_password",
            "is_active": True,
            "created_at": __import__('datetime').datetime.utcnow(),
            "updated_at": __import__('datetime').datetime.utcnow()
        })
        self.user_id = str(user.inserted_id)
        
        # Registrar e fazer login
        reg_response = client.post("/api/v1/auth/register", json={
            "email": "test_trans@example.com",
            "full_name": "Test Transaction",
            "password": "MyPassword123!"
        })
        self.token = reg_response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        
        # Registrar cartão
        card_response = client.post("/api/v1/cards/register",
            headers=self.headers,
            json={
                "card_number": "4532015112830366",
                "cardholder_name": "Test User",
                "expiry_month": 12,
                "expiry_year": 2026,
                "cvv": "123"
            }
        )
        self.card_id = card_response.json()["id"]
        
        yield
        
        # Cleanup
        db.users.delete_many({})
        db.cards.delete_many({})
        db.transactions.delete_many({})
    
    def test_create_transaction_success(self):
        """Teste de criação de transação bem-sucedida"""
        response = client.post("/api/v1/transactions/create",
            headers=self.headers,
            json={
                "card_id": self.card_id,
                "amount": 100.00,
                "currency": "USD",
                "description": "Test transaction",
                "reference_id": "REF123456"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == 100.00
        assert data["status"] == "completed"
    
    def test_create_transaction_invalid_amount(self):
        """Teste de criação com valor inválido"""
        response = client.post("/api/v1/transactions/create",
            headers=self.headers,
            json={
                "card_id": self.card_id,
                "amount": 0,
                "currency": "USD",
                "description": "Test transaction",
                "reference_id": "REF123456"
            }
        )
        assert response.status_code == 422
    
    def test_get_transaction(self):
        """Teste de obter transação"""
        # Criar transação
        create_response = client.post("/api/v1/transactions/create",
            headers=self.headers,
            json={
                "card_id": self.card_id,
                "amount": 100.00,
                "currency": "USD",
                "description": "Test transaction",
                "reference_id": "REF123456"
            }
        )
        transaction_id = create_response.json()["id"]
        
        # Obter transação
        response = client.get(f"/api/v1/transactions/{transaction_id}",
            headers=self.headers
        )
        assert response.status_code == 200
        assert response.json()["amount"] == 100.00