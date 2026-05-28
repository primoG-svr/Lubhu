from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Optional
from bson import ObjectId
from app.schemas import CardRegister, CardResponse, CardValidationResponse, CardValidation
from app.security import CardValidationService, EncryptionService, JWTService
from app.database import get_database

router = APIRouter(prefix="/cards", tags=["Cards"])

def get_user_id(authorization: str = Header(None)) -> str:
    """Extrai user_id do JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não fornecido"
        )
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = JWTService.verify_token(token)
        return payload.get("sub")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

@router.post("/register", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def register_card(
    card_data: CardRegister,
    db=Depends(get_database),
    user_id: str = Depends(get_user_id)
):
    """Registrar novo cartão"""
    
    # Validar cartão
    if not CardValidationService.validate_card_number(card_data.card_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Número de cartão inválido"
        )
    
    if not CardValidationService.validate_cvv(card_data.cvv):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CVV inválido"
        )
    
    if not CardValidationService.validate_expiry(card_data.expiry_month, card_data.expiry_year):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cartão expirado"
        )
    
    # Criptografar dados sensíveis
    encrypted_card = EncryptionService.encrypt_card_number(card_data.card_number)
    encrypted_cvv = EncryptionService.encrypt_card_number(card_data.cvv)
    last_four = card_data.card_number[-4:]
    card_type = CardValidationService.get_card_type(card_data.card_number)
    
    # Se é cartão padrão, desativar outros
    if card_data.is_default:
        db.cards.update_many(
            {"user_id": user_id},
            {"$set": {"is_default": False}}
        )
    
    # Inserir cartão
    card_doc = {
        "user_id": user_id,
        "card_number": encrypted_card,
        "cvv": encrypted_cvv,
        "cardholder_name": card_data.cardholder_name,
        "expiry_month": card_data.expiry_month,
        "expiry_year": card_data.expiry_year,
        "card_type": card_type,
        "last_four": last_four,
        "is_default": card_data.is_default,
        "is_active": True,
        "created_at": __import__('datetime').datetime.utcnow(),
        "updated_at": __import__('datetime').datetime.utcnow()
    }
    
    result = db.cards.insert_one(card_doc)
    
    return {
        "id": str(result.inserted_id),
        "cardholder_name": card_data.cardholder_name,
        "last_four": last_four,
        "expiry_month": card_data.expiry_month,
        "expiry_year": card_data.expiry_year,
        "card_type": card_type,
        "is_default": card_data.is_default,
        "is_active": True,
        "created_at": card_doc["created_at"]
    }

@router.post("/validate", response_model=CardValidationResponse)
async def validate_card(card_data: CardValidation):
    """Validar dados do cartão"""
    
    is_valid = True
    messages = []
    
    # Validar número
    if not CardValidationService.validate_card_number(card_data.card_number):
        is_valid = False
        messages.append("Número de cartão inválido")
    
    # Validar CVV
    if not CardValidationService.validate_cvv(card_data.cvv):
        is_valid = False
        messages.append("CVV inválido")
    
    # Validar expiração
    if not CardValidationService.validate_expiry(card_data.expiry_month, card_data.expiry_year):
        is_valid = False
        messages.append("Cartão expirado")
    
    card_type = CardValidationService.get_card_type(card_data.card_number)
    last_four = card_data.card_number[-4:]
    
    return {
        "is_valid": is_valid,
        "card_type": card_type,
        "last_four": last_four,
        "message": " | ".join(messages) if messages else "Cartão válido"
    }

@router.get("/list", status_code=status.HTTP_200_OK)
async def list_cards(
    db=Depends(get_database),
    user_id: str = Depends(get_user_id)
):
    """Listar cartões do usuário"""
    cards = list(db.cards.find({"user_id": user_id, "is_active": True}))
    
    return {
        "total": len(cards),
        "cards": [
            {
                "id": str(card["_id"]),
                "cardholder_name": card["cardholder_name"],
                "last_four": card["last_four"],
                "card_type": card["card_type"],
                "expiry_month": card["expiry_month"],
                "expiry_year": card["expiry_year"],
                "is_default": card["is_default"],
                "created_at": card["created_at"]
            }
            for card in cards
        ]
    }