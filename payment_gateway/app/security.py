from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import os
from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class EncryptionService:
    """Serviço de criptografia para dados sensíveis"""
    
    @staticmethod
    def derive_key(password: str, salt: bytes = b'') -> bytes:
        """Deriva uma chave usando PBKDF2"""
        if not salt:
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    @staticmethod
    def encrypt_card_number(card_number: str) -> str:
        """Criptografa número de cartão"""
        if not settings.ENCRYPT_SENSITIVE_DATA:
            return card_number
        
        key = EncryptionService.derive_key(settings.ENCRYPTION_KEY)
        cipher = Fernet(key)
        encrypted = cipher.encrypt(card_number.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt_card_number(encrypted_card: str) -> str:
        """Descriptografa número de cartão"""
        if not settings.ENCRYPT_SENSITIVE_DATA:
            return encrypted_card
        
        try:
            key = EncryptionService.derive_key(settings.ENCRYPTION_KEY)
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_card.encode())
            return decrypted.decode()
        except Exception:
            raise ValueError("Falha na descriptografia do cartão")
    
    @staticmethod
    def mask_card_number(card_number: str) -> str:
        """Mascara número do cartão (últimos 4 dígitos visíveis)"""
        return f"****-****-****-{card_number[-4:]}"

class JWTService:
    """Serviço de autenticação JWT"""
    
    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Cria token de acesso JWT"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Cria token de refresh JWT"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verifica validade do token JWT"""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            raise ValueError("Token inválido ou expirado")

class PasswordService:
    """Serviço de gerenciamento de senhas"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash de senha com bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica senha contra hash"""
        return pwd_context.verify(plain_password, hashed_password)

class CardValidationService:
    """Serviço de validação de cartões"""
    
    @staticmethod
    def validate_card_number(card_number: str) -> bool:
        """Valida número de cartão usando Algoritmo de Luhn"""
        card_number = card_number.replace(" ", "").replace("-", "")
        
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False
        
        # Algoritmo de Luhn
        digits = [int(d) for d in card_number]
        checksum = 0
        
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        
        return checksum % 10 == 0
    
    @staticmethod
    def validate_cvv(cvv: str) -> bool:
        """Valida CVV (3-4 dígitos)"""
        return cvv.isdigit() and 3 <= len(cvv) <= 4
    
    @staticmethod
    def validate_expiry(month: int, year: int) -> bool:
        """Valida data de expiração do cartão"""
        if not (1 <= month <= 12):
            return False
        
        current_date = datetime.utcnow()
        expiry_date = datetime(year + 2000, month, 1)
        
        return expiry_date > current_date
    
    @staticmethod
    def get_card_type(card_number: str) -> str:
        """Identifica tipo de cartão"""
        card_number = card_number.replace(" ", "").replace("-", "")
        
        if card_number.startswith("4"):
            return "VISA"
        elif card_number.startswith(("51", "52", "53", "54", "55")):
            return "MASTERCARD"
        elif card_number.startswith(("34", "37")):
            return "AMEX"
        elif card_number.startswith("6011"):
            return "DISCOVER"
        else:
            return "UNKNOWN"