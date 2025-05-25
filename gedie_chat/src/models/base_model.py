"""
Model base para todos os models do GEDIE
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr
from config.database_config import Base

class BaseModel(Base):
    """Classe base para todos os models"""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    @declared_attr
    def __tablename__(cls):
        # Converter CamelCase para snake_case
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    def to_dict(self):
        """Converter model para dicionário"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def save(self, db_session):
        """Salvar no banco de dados"""
        db_session.add(self)
        db_session.commit()
        db_session.refresh(self)
        return self
    
    def delete(self, db_session):
        """Remover do banco de dados"""
        db_session.delete(self)
        db_session.commit()
        return True