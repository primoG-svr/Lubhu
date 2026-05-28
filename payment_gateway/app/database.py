from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class Database:
    """Gerenciador de conexão com MongoDB"""
    
    _client: MongoClient = None
    _db = None
    
    @classmethod
    def connect(cls):
        """Conecta ao MongoDB"""
        try:
            cls._client = MongoClient(settings.DATABASE_URL)
            cls._db = cls._client[settings.DATABASE_NAME]
            
            # Test connection
            cls._client.admin.command('ping')
            logger.info("MongoDB conectado com sucesso")
            
            # Create indexes
            cls._create_indexes()
            
        except ConnectionFailure as e:
            logger.error(f"Erro ao conectar ao MongoDB: {e}")
            raise
    
    @classmethod
    def disconnect(cls):
        """Desconecta do MongoDB"""
        if cls._client:
            cls._client.close()
            logger.info("MongoDB desconectado")
    
    @classmethod
    def get_db(cls):
        """Retorna instância do banco de dados"""
        if cls._db is None:
            cls.connect()
        return cls._db
    
    @classmethod
    def _create_indexes(cls):
        """Cria índices para melhor performance"""
        db = cls._db
        
        # Users
        db.users.create_index([("email", ASCENDING)], unique=True)
        db.users.create_index([("created_at", DESCENDING)])
        
        # Cards
        db.cards.create_index([("user_id", ASCENDING)])
        db.cards.create_index([("user_id", ASCENDING), ("is_default", ASCENDING)])
        
        # Transactions
        db.transactions.create_index([("user_id", ASCENDING)])
        db.transactions.create_index([("reference_id", ASCENDING)], unique=True)
        db.transactions.create_index([("created_at", DESCENDING)])
        db.transactions.create_index([("status", ASCENDING)])
        db.transactions.create_index([("is_fraud_detected", ASCENDING)])
        
        # Webhooks
        db.webhooks.create_index([("user_id", ASCENDING)])
        
        # Audit Logs
        db.audit_logs.create_index([("user_id", ASCENDING)])
        db.audit_logs.create_index([("created_at", DESCENDING)])
        db.audit_logs.create_index([("resource_type", ASCENDING), ("resource_id", ASCENDING)])
        
        logger.info("Índices criados com sucesso")

def get_database():
    """Dependency para obter instância do banco"""
    return Database.get_db()