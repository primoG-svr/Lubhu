from fastapi import APIRouter, HTTPException, status, Depends, Header
from datetime import datetime
from bson import ObjectId
import uuid
from app.schemas import TransactionCreate, TransactionResponse, RefundRequest, RefundResponse
from app.models import TransactionStatus
from app.security import JWTService
from app.database import get_database

router = APIRouter(prefix="/transactions", tags=["Transactions"])

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

@router.post("/create", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db=Depends(get_database),
    user_id: str = Depends(get_user_id)
):
    """Criar nova transação"""
    
    # Validar cartão
    card_id = transaction_data.card_id
    card = None
    
    if card_id:
        card = db.cards.find_one({
            "_id": ObjectId(card_id),
            "user_id": user_id,
            "is_active": True
        })
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cartão não encontrado"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cartão é obrigatório"
        )
    
    # Criar documento de transação
    transaction_doc = {
        "user_id": user_id,
        "card_id": card_id,
        "amount": transaction_data.amount,
        "currency": transaction_data.currency,
        "status": TransactionStatus.PROCESSING.value,
        "payment_method": "credit_card",
        "description": transaction_data.description,
        "reference_id": transaction_data.reference_id,
        "metadata": transaction_data.metadata,
        "ip_address": "127.0.0.1",
        "user_agent": "API",
        "fraud_score": 0.0,
        "is_fraud_detected": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "completed_at": None
    }
    
    result = db.transactions.insert_one(transaction_doc)
    transaction_id = str(result.inserted_id)
    
    # Simular processamento bem-sucedido
    db.transactions.update_one(
        {"_id": ObjectId(transaction_id)},
        {
            "$set": {
                "status": TransactionStatus.COMPLETED.value,
                "completed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    transaction_doc["_id"] = ObjectId(transaction_id)
    transaction_doc["status"] = TransactionStatus.COMPLETED.value
    transaction_doc["completed_at"] = datetime.utcnow()
    
    return {
        "id": transaction_id,
        "amount": transaction_data.amount,
        "currency": transaction_data.currency,
        "status": TransactionStatus.COMPLETED,
        "description": transaction_data.description,
        "reference_id": transaction_data.reference_id,
        "card_last_four": card["last_four"],
        "fraud_score": 0.0,
        "is_fraud_detected": False,
        "created_at": transaction_doc["created_at"],
        "completed_at": transaction_doc["completed_at"]
    }

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    db=Depends(get_database),
    user_id: str = Depends(get_user_id)
):
    """Obter detalhes de uma transação"""
    
    transaction = db.transactions.find_one({
        "_id": ObjectId(transaction_id),
        "user_id": user_id
    })
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não encontrada"
        )
    
    card = db.cards.find_one({"_id": ObjectId(transaction["card_id"])})
    
    return {
        "id": str(transaction["_id"]),
        "amount": transaction["amount"],
        "currency": transaction["currency"],
        "status": transaction["status"],
        "description": transaction["description"],
        "reference_id": transaction["reference_id"],
        "card_last_four": card["last_four"],
        "fraud_score": transaction["fraud_score"],
        "is_fraud_detected": transaction["is_fraud_detected"],
        "created_at": transaction["created_at"],
        "completed_at": transaction.get("completed_at")
    }

@router.get("/")
async def list_transactions(
    skip: int = 0,
    limit: int = 10,
    status_filter: str = None,
    db=Depends(get_database),
    user_id: str = Depends(get_user_id)
):
    """Listar transações do usuário"""
    
    query = {"user_id": user_id}
    if status_filter:
        query["status"] = status_filter
    
    transactions = list(db.transactions.find(query).skip(skip).limit(limit))
    total = db.transactions.count_documents(query)
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "per_page": limit,
        "transactions": [
            {
                "id": str(t["_id"]),
                "amount": t["amount"],
                "currency": t["currency"],
                "status": t["status"],
                "description": t["description"],
                "reference_id": t["reference_id"],
                "card_last_four": t.get("card_last_four", "****"),
                "fraud_score": t["fraud_score"],
                "is_fraud_detected": t["is_fraud_detected"],
                "created_at": t["created_at"],
                "completed_at": t.get("completed_at")
            }
            for t in transactions
        ]
    }

@router.put("/{transaction_id}/refund", response_model=RefundResponse)
async def refund_transaction(
    transaction_id: str,
    refund_data: RefundRequest,
    db=Depends(get_database),
    user_id: str = Depends(get_user_id)
):
    """Reembolsar transação"""
    
    transaction = db.transactions.find_one({
        "_id": ObjectId(transaction_id),
        "user_id": user_id
    })
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não encontrada"
        )
    
    if transaction["status"] != TransactionStatus.COMPLETED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas transações completas podem ser reembolsadas"
        )
    
    # Atualizar transação
    db.transactions.update_one(
        {"_id": ObjectId(transaction_id)},
        {
            "$set": {
                "status": TransactionStatus.REFUNDED.value,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    refund_id = str(uuid.uuid4())
    refund_amount = refund_data.partial_amount or transaction["amount"]
    
    return {
        "transaction_id": transaction_id,
        "refund_id": refund_id,
        "amount": refund_amount,
        "status": "completed",
        "created_at": datetime.utcnow()
    }