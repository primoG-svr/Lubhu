from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field

class TransactionStatus(str, Enum):
    """Status de transação"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    """Método de pagamento"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    DIGITAL_WALLET = "digital_wallet"

class CardType(str, Enum):
    """Tipo de cartão"""
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    AMEX = "AMEX"
    DISCOVER = "DISCOVER"
    ELO = "ELO"

class User(BaseModel):
    """Modelo de usuário"""
    id: Optional[str] = Field(default=None, alias="_id")
    email: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True

class Card(BaseModel):
    """Modelo de cartão"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    card_number: str  # Criptografado
    cvv: str  # Criptografado
    cardholder_name: str
    expiry_month: int
    expiry_year: int
    card_type: CardType
    last_four: str  # Últimos 4 dígitos visíveis
    is_default: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True

class Transaction(BaseModel):
    """Modelo de transação"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    card_id: str
    amount: float
    currency: str = "USD"
    status: TransactionStatus = TransactionStatus.PENDING
    payment_method: PaymentMethod
    description: str
    reference_id: str  # Identificador único externo
    metadata: dict = {}
    ip_address: str
    user_agent: str
    fraud_score: float = 0.0
    is_fraud_detected: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True

class Webhook(BaseModel):
    """Modelo de webhook"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    url: str
    events: List[str] = ["transaction.completed", "transaction.failed"]
    is_active: bool = True
    secret: str  # Para validação de assinatura
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True

class AuditLog(BaseModel):
    """Modelo de log de auditoria"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    changes: dict = {}
    ip_address: str
    user_agent: str
    status: str = "success"
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True