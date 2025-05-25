"""
Model para categorias de gastos
"""

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from loguru import logger
import enum

class TipoCategoria(enum.Enum):
    DESPESA = "despesa"
    RECEITA = "receita"

class Category(BaseModel):
    """Model de categoria"""
    
    __tablename__ = 'categories'
    
    nome = Column(String(50), nullable=False)
    icone = Column(String(10), nullable=False)
    cor = Column(String(7), default='#3498db', nullable=False)
    tipo = Column(Enum(TipoCategoria), default=TipoCategoria.DESPESA, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, nome='{self.nome}', icone='{self.icone}')>"
    
    @classmethod
    def create_default_categories(cls, db_session, user_id):
        """Criar categorias padrão para novo usuário"""
        default_categories = [
            {"nome": "Alimentação", "icone": "🍔", "cor": "#e74c3c"},
            {"nome": "Transporte", "icone": "🚗", "cor": "#3498db"},
            {"nome": "Casa", "icone": "🏠", "cor": "#2ecc71"},
            {"nome": "Saúde", "icone": "💊", "cor": "#e67e22"},
            {"nome": "Lazer", "icone": "🎬", "cor": "#9b59b6"},
            {"nome": "Roupas", "icone": "👕", "cor": "#f39c12"},
            {"nome": "Educação", "icone": "📚", "cor": "#34495e"},
            {"nome": "Outros", "icone": "💳", "cor": "#95a5a6"},
        ]
        
        try:
            created_categories = []
            for cat_data in default_categories:
                category = cls(
                    nome=cat_data["nome"],
                    icone=cat_data["icone"],
                    cor=cat_data["cor"],
                    user_id=user_id,
                    tipo=TipoCategoria.DESPESA
                )
                created_categories.append(category.save(db_session))
            
            logger.info(f"✅ {len(created_categories)} categorias padrão criadas para usuário {user_id}")
            return created_categories
        except Exception as e:
            logger.error(f"Erro ao criar categorias padrão: {e}")
            return []
    
    @classmethod
    def get_user_categories(cls, db_session, user_id, tipo=None):
        """Obter categorias do usuário"""
        try:
            query = db_session.query(cls).filter(
                cls.user_id == user_id,
                cls.ativo == True
            )
            
            if tipo:
                query = query.filter(cls.tipo == tipo)
            
            return query.order_by(cls.nome).all()
        except Exception as e:
            logger.error(f"Erro ao buscar categorias do usuário {user_id}: {e}")
            return []