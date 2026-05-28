import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Database

client = TestClient(app)

class TestAuth:
    """Testes de autenticação"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        Database.connect()
        db = Database.get_db()
        # Limpar usuários
        db.users.delete_many({})
        yield
        db.users.delete_many({})
    
    def test_register_success(self):
        """Teste de registro bem-sucedido"""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "MyPassword123!"
        })
        assert response.status_code == 201
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
    
    def test_register_duplicate_email(self):
        """Teste de registro com email duplicado"""
        # Primeiro registro
        client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "MyPassword123!"
        })
        
        # Segundo registro com mesmo email
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "full_name": "Test User 2",
            "password": "MyPassword456!"
        })
        assert response.status_code == 400
    
    def test_register_weak_password(self):
        """Teste de registro com senha fraca"""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "weak"
        })
        assert response.status_code == 422
    
    def test_login_success(self):
        """Teste de login bem-sucedido"""
        # Registrar primeiro
        client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "MyPassword123!"
        })
        
        # Fazer login
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "MyPassword123!"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_wrong_password(self):
        """Teste de login com senha errada"""
        # Registrar primeiro
        client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "MyPassword123!"
        })
        
        # Tentar login com senha errada
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        })
        assert response.status_code == 401