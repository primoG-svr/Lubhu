import pytest
from app.security import (
    CardValidationService,
    EncryptionService,
    JWTService,
    PasswordService
)
from datetime import datetime, timedelta

class TestCardValidation:
    """Testes de validação de cartão"""
    
    def test_valid_card_number_visa(self):
        """Teste de número válido Visa"""
        assert CardValidationService.validate_card_number("4532015112830366") is True
    
    def test_invalid_card_number(self):
        """Teste de número inválido"""
        assert CardValidationService.validate_card_number("1234567890123456") is False
    
    def test_valid_cvv(self):
        """Teste de CVV válido"""
        assert CardValidationService.validate_cvv("123") is True
        assert CardValidationService.validate_cvv("1234") is True
    
    def test_invalid_cvv(self):
        """Teste de CVV inválido"""
        assert CardValidationService.validate_cvv("12") is False
        assert CardValidationService.validate_cvv("12345") is False
    
    def test_valid_expiry(self):
        """Teste de data de expiração válida"""
        future_year = datetime.utcnow().year + 2
        assert CardValidationService.validate_expiry(12, future_year) is True
    
    def test_invalid_expiry_month(self):
        """Teste de mês inválido"""
        assert CardValidationService.validate_expiry(13, 2025) is False
    
    def test_expired_card(self):
        """Teste de cartão expirado"""
        assert CardValidationService.validate_expiry(1, 2020) is False
    
    def test_card_type_visa(self):
        """Teste de identificação Visa"""
        assert CardValidationService.get_card_type("4532015112830366") == "VISA"
    
    def test_card_type_mastercard(self):
        """Teste de identificação Mastercard"""
        assert CardValidationService.get_card_type("5425233010103442") == "MASTERCARD"

class TestEncryption:
    """Testes de criptografia"""
    
    def test_encrypt_decrypt_card(self):
        """Teste de criptografia e descriptografia"""
        original = "4532015112830366"
        encrypted = EncryptionService.encrypt_card_number(original)
        decrypted = EncryptionService.decrypt_card_number(encrypted)
        assert decrypted == original
    
    def test_mask_card_number(self):
        """Teste de máscara de número de cartão"""
        masked = EncryptionService.mask_card_number("4532015112830366")
        assert masked == "****-****-****-0366"

class TestJWT:
    """Testes de JWT"""
    
    def test_create_access_token(self):
        """Teste de criação de token de acesso"""
        token = JWTService.create_access_token({"sub": "user123"})
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_valid_token(self):
        """Teste de verificação de token válido"""
        data = {"sub": "user123", "email": "test@example.com"}
        token = JWTService.create_access_token(data)
        payload = JWTService.verify_token(token)
        assert payload["sub"] == "user123"
        assert payload["email"] == "test@example.com"
    
    def test_verify_invalid_token(self):
        """Teste de verificação de token inválido"""
        with pytest.raises(ValueError):
            JWTService.verify_token("invalid.token.here")

class TestPassword:
    """Testes de senha"""
    
    def test_hash_password(self):
        """Teste de hash de senha"""
        password = "MyPassword123!"
        hashed = PasswordService.hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password(self):
        """Teste de verificação de senha"""
        password = "MyPassword123!"
        hashed = PasswordService.hash_password(password)
        assert PasswordService.verify_password(password, hashed) is True
    
    def test_verify_wrong_password(self):
        """Teste de verificação com senha errada"""
        password = "MyPassword123!"
        hashed = PasswordService.hash_password(password)
        assert PasswordService.verify_password("WrongPassword123!", hashed) is False