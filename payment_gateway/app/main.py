from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import logging
from app.config import get_settings
from app.database import Database
from app.api import auth, transactions, cards, analytics

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    logger.info("Iniciando aplicação...")
    Database.connect()
    yield
    # Shutdown
    logger.info("Encerrando aplicação...")
    Database.disconnect()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Gateway de Pagamento Segura com Validação e Testes",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
)

# Custom Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global para exceções"""
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Um erro interno ocorreu",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Routes
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(cards.router, prefix=settings.API_V1_STR, tags=["Cards"])
app.include_router(transactions.router, prefix=settings.API_V1_STR, tags=["Transactions"])
app.include_router(analytics.router, prefix=settings.API_V1_STR, tags=["Analytics"])

# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Payment Gateway API",
        "version": settings.VERSION,
        "docs": "/docs",
        "openapi_schema": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )