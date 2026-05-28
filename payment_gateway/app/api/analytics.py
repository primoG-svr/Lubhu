from fastapi import APIRouter, Depends, Header, HTTPException, status
from datetime import datetime, timedelta
from app.security import JWTService
from app.database import get_database
from app.models import TransactionStatus

router = APIRouter(prefix="/analytics", tags=["Analytics"])

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

@router.get("/summary")
async def get_summary(
    days: int = 30,
    db=Depends(get_database),
    user_id: str = Depends(get_user_id)
):
    """Obter resumo de analytics"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Buscar transações
    transactions = list(db.transactions.find({
        "user_id": user_id,
        "created_at": {"$gte": start_date}
    }))
    
    # Calcular estatísticas
    total_transactions = len(transactions)
    total_amount = sum(t["amount"] for t in transactions)
    completed = sum(1 for t in transactions if t["status"] == TransactionStatus.COMPLETED.value)
    failed = sum(1 for t in transactions if t["status"] == TransactionStatus.FAILED.value)
    refunded = sum(1 for t in transactions if t["status"] == TransactionStatus.REFUNDED.value)
    refunded_amount = sum(t["amount"] for t in transactions if t["status"] == TransactionStatus.REFUNDED.value)
    fraud_detected = sum(1 for t in transactions if t["is_fraud_detected"])
    
    avg_amount = total_amount / total_transactions if total_transactions > 0 else 0
    fraud_rate = (fraud_detected / total_transactions * 100) if total_transactions > 0 else 0
    
    # Agrupar por status
    by_status = {
        "completed": completed,
        "failed": failed,
        "refunded": refunded,
        "pending": total_transactions - completed - failed - refunded
    }
    
    # Agrupar por moeda
    by_currency = {}
    for t in transactions:
        currency = t["currency"]
        if currency not in by_currency:
            by_currency[currency] = {"count": 0, "amount": 0}
        by_currency[currency]["count"] += 1
        by_currency[currency]["amount"] += t["amount"]
    
    return {
        "period": f"{days} days",
        "stats": {
            "total_transactions": total_transactions,
            "total_amount": round(total_amount, 2),
            "completed_transactions": completed,
            "failed_transactions": failed,
            "pending_transactions": total_transactions - completed - failed - refunded,
            "refunded_amount": round(refunded_amount, 2),
            "average_transaction_amount": round(avg_amount, 2),
            "fraud_detection_rate": round(fraud_rate, 2)
        },
        "by_status": by_status,
        "by_currency": by_currency
    }