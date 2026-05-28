from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TransactionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

# ============ Auth Schemas ============

class UserRegister(BaseModel):
    """Schema para registro de usuário"""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        if not any(char.isdigit() for char in v):
            raise ValueError('Senha deve conter pelo menos um dígito')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in v):
            raise ValueError('Senha deve conter pelo menos um caractere especial')
        return v

class UserLogin(BaseModel):
    """Schema para login de usuário"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema de resposta do usuário"""
    id: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Schema de resposta de token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# ============ Card Schemas ============

class CardRegister(BaseModel):
    """Schema para registrar novo cartão"""
    card_number: str = Field(..., min_length=13, max_length=19)
    cardholder_name: str = Field(..., min_length=2, max_length=100)
    expiry_month: int = Field(..., ge=1, le=12)
    expiry_year: int = Field(..., ge=2024, le=2099)
    cvv: str = Field(..., min_length=3, max_length=4)
    is_default: bool = False
    
    @validator('card_number')
    def validate_card_number(cls, v):
        v = v.replace(" ", "").replace("-", "")
        if not v.isdigit():
            raise ValueError('Número de cartão deve conter apenas dígitos')
        return v
    
    @validator('cvv')
    def validate_cvv(cls, v):
        if not v.isdigit():
            raise ValueError('CVV deve conter apenas dígitos')
        return v

class CardResponse(BaseModel):
    """Schema de resposta do cartão"""
    id: str
    cardholder_name: str
    last_four: str
    expiry_month: int
    expiry_year: int
    card_type: str
    is_default: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CardValidation(BaseModel):
    """Schema para validação de cartão"""
    card_number: str
    expiry_month: int
    expiry_year: int
    cvv: str

class CardValidationResponse(BaseModel):
    """Schema de resposta de validação de cartão"""
    is_valid: bool
    card_type: str
    last_four: str
    message: str

# ============ Transaction Schemas ============

class TransactionCreate(BaseModel):
    """Schema para criar transação"""
    card_id: Optional[str] = None
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    description: str = Field(..., min_length=1, max_length=500)
    reference_id: str = Field(..., min_length=1, max_length=100)
    metadata: dict = {}
    card_data: Optional[CardRegister] = None  # Para usar cartão novo inline
    
    @validator('amount')
    def validate_amount(cls, v):
        if v < 0.01:
            raise ValueError('Valor mínimo é 0.01')
        if v > 999999.99:
            raise ValueError('Valor máximo é 999999.99')
        return round(v, 2)

class TransactionResponse(BaseModel):
    """Schema de resposta de transação"""
    id: str
    amount: float
    currency: str
    status: TransactionStatus
    description: str
    reference_id: str
    card_last_four: str
    fraud_score: float
    is_fraud_detected: bool
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    """Schema de resposta de lista de transações"""
    total: int
    page: int
    per_page: int
    transactions: List[TransactionResponse]

class RefundRequest(BaseModel):
    """Schema para requisição de reembolso"""
    reason: str = Field(..., min_length=1, max_length=500)
    partial_amount: Optional[float] = None

class RefundResponse(BaseModel):
    """Schema de resposta de reembolso"""
    transaction_id: str
    refund_id: str
    amount: float
    status: str
    created_at: datetime

# ============ Webhook Schemas ============

class WebhookCreate(BaseModel):
    """Schema para criar webhook"""
    url: str = Field(..., min_length=10)
    events: List[str] = ["transaction.completed", "transaction.failed"]

class WebhookResponse(BaseModel):
    """Schema de resposta de webhook"""
    id: str
    url: str
    events: List[str]
    is_active: bool
    created_at: datetime

# ============ Analytics Schemas ============

class TransactionStats(BaseModel):
    """Schema de estatísticas de transações"""
    total_transactions: int
    total_amount: float
    completed_transactions: int
    failed_transactions: int
    pending_transactions: int
    refunded_amount: float
    average_transaction_amount: float
    fraud_detection_rate: float

class AnalyticsResponse(BaseModel):
    """Schema de resposta de analytics"""
    period: str
    stats: TransactionStats
    by_status: dict
    by_currency: dict

# ============ Error Schemas ============

class ErrorResponse(BaseModel):
    """Schema de resposta de erro"""
    error: str
    message: str
    status_code: int
    timestamp: datetime