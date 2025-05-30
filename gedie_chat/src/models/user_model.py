"""
Model para usuários do sistema - VERSÃO COM CÓDIGO DE ACESSO
"""

from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from loguru import logger

class User(BaseModel):
    """Model de usuário"""
    
    __tablename__ = 'users'
    
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    timezone = Column(String(50), default='America/Sao_Paulo', nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    codigo_acesso = Column(String(6), nullable=True)  # NOVO CAMPO
    
    # Relacionamentos
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, nome='{self.nome}')>"
    
    @classmethod
    def get_by_telegram_id(cls, db_session, telegram_id):
        """Buscar usuário pelo Telegram ID"""
        try:
            user = db_session.query(cls).filter(cls.telegram_id == telegram_id).first()
            return user
        except Exception as e:
            logger.error(f"Erro ao buscar usuário {telegram_id}: {e}")
            return None
    
    @classmethod
    def create_user(cls, db_session, telegram_id, nome, timezone='America/Sao_Paulo'):
        """Criar novo usuário"""
        try:
            user = cls(
                telegram_id=telegram_id,
                nome=nome,
                timezone=timezone
            )
            return user.save(db_session)
        except Exception as e:
            logger.error(f"Erro ao criar usuário {telegram_id}: {e}")
            return None
    
    @classmethod
    def update_access_code(cls, db_session, user_id, codigo_acesso):
        """Atualizar código de acesso do usuário"""
        try:
            user = db_session.query(cls).filter(cls.id == user_id).first()
            if user:
                user.codigo_acesso = codigo_acesso
                db_session.commit()
                db_session.refresh(user)
                logger.info(f"Código de acesso atualizado para usuário {user_id}")
                return True
            else:
                logger.error(f"Usuário {user_id} não encontrado para atualizar código")
                return False
        except Exception as e:
            logger.error(f"Erro ao atualizar código de acesso {user_id}: {e}")
            db_session.rollback()
            return False
    
    @classmethod
    def get_by_telegram_id_and_code(cls, db_session, telegram_id, codigo_acesso):
        """Buscar usuário por Telegram ID e código de acesso (para login web)"""
        try:
            user = db_session.query(cls).filter(
                cls.telegram_id == telegram_id,
                cls.codigo_acesso == codigo_acesso,
                cls.ativo == True
            ).first()
            return user
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por ID e código {telegram_id}: {e}")
            return None
    
    def is_active(self):
        """Verificar se usuário está ativo"""
        return self.ativo
    
    def has_access_code(self):
        """Verificar se usuário possui código de acesso"""
        return self.codigo_acesso is not None and len(self.codigo_acesso) == 6
    
    def get_categories(self, db_session):
        """Obter categorias do usuário"""
        from models.category_model import Category
        return db_session.query(Category).filter(
            Category.user_id == self.id,
            Category.ativo == True
        ).all()