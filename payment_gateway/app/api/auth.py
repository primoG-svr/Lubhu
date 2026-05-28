from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from app.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.security import JWTService, PasswordService
from app.database import get_database
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
settings = get_settings()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db=Depends(get_database)):
    """Registrar novo usuário"""
    try:
        # Verificar se usuário já existe
        existing_user = db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Criar novo usuário
        hashed_password = PasswordService.hash_password(user_data.password)
        user_doc = {
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": __import__('datetime').datetime.utcnow(),
            "updated_at": __import__('datetime').datetime.utcnow()
        }
        
        result = db.users.insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        # Criar tokens
        access_token = JWTService.create_access_token(
            data={"sub": user_id, "email": user_data.email}
        )
        refresh_token = JWTService.create_refresh_token(
            data={"sub": user_id, "email": user_data.email}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar usuário: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db=Depends(get_database)):
    """Login de usuário"""
    # Buscar usuário
    user = db.users.find_one({"email": user_data.email})
    if not user or not PasswordService.verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    user_id = str(user["_id"])
    
    # Criar tokens
    access_token = JWTService.create_access_token(
        data={"sub": user_id, "email": user["email"]}
    )
    refresh_token = JWTService.create_refresh_token(
        data={"sub": user_id, "email": user["email"]}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token: str, db=Depends(get_database)):
    """Refresh do token de acesso"""
    try:
        payload = JWTService.verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Buscar usuário
        user = db.users.find_one({"_id": __import__('bson').ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Criar novo token
        access_token = JWTService.create_access_token(
            data={"sub": user_id, "email": user["email"]}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": token,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )