"""
Configuração do banco de dados MySQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
from loguru import logger

# Configurações do banco
MYSQL_HOST = config('MYSQL_HOST', default='localhost')
MYSQL_PORT = config('MYSQL_PORT', default=3306, cast=int)
MYSQL_USER = config('MYSQL_USER', default='gedie_user')
MYSQL_PASSWORD = config('MYSQL_PASSWORD')
MYSQL_DATABASE = config('MYSQL_DATABASE', default='gedie_db')

# URL de conexão
DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    f"?charset=utf8mb4"
)

# Engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    echo=config('DEBUG', default=False, cast=bool)
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os models
Base = declarative_base()

def get_db_session():
    """Criar nova sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Testar conexão com o banco"""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            logger.info("✅ Conexão com MySQL estabelecida com sucesso!")
            return True
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com MySQL: {e}")
        return False

def create_tables():
    """Criar todas as tabelas no banco"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        return False