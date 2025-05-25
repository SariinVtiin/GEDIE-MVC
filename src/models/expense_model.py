"""
Model para gastos/receitas
"""

from datetime import date, datetime
from sqlalchemy import Column, Numeric, Text, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from loguru import logger

class Expense(BaseModel):
    """Model de gasto/receita"""
    
    __tablename__ = 'expenses'
    
    valor = Column(Numeric(10, 2), nullable=False)
    descricao = Column(Text)
    data_gasto = Column(Date, default=date.today, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relacionamentos
    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")
    
    def __repr__(self):
        return f"<Expense(id={self.id}, valor={self.valor}, categoria='{self.category.nome if self.category else 'N/A'}')>"
    
    @classmethod
    def create_expense(cls, db_session, user_id, category_id, valor, descricao=None, data_gasto=None):
        """Criar novo gasto"""
        try:
            expense = cls(
                user_id=user_id,
                category_id=category_id,
                valor=valor,
                descricao=descricao,
                data_gasto=data_gasto or date.today()
            )
            return expense.save(db_session)
        except Exception as e:
            logger.error(f"Erro ao criar gasto: {e}")
            return None
    
    @classmethod
    def get_user_expenses(cls, db_session, user_id, data_inicio=None, data_fim=None):
        """Obter gastos do usuário por período"""
        try:
            query = db_session.query(cls).filter(cls.user_id == user_id)
            
            if data_inicio:
                query = query.filter(cls.data_gasto >= data_inicio)
            
            if data_fim:
                query = query.filter(cls.data_gasto <= data_fim)
            
            return query.order_by(cls.data_gasto.desc(), cls.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Erro ao buscar gastos do usuário {user_id}: {e}")
            return []
    
    @classmethod
    def get_today_expenses(cls, db_session, user_id):
        """Obter gastos de hoje"""
        today = date.today()
        return cls.get_user_expenses(db_session, user_id, today, today)
    
    @classmethod
    def get_month_total(cls, db_session, user_id, mes=None, ano=None):
        """Obter total de gastos do mês"""
        try:
            if not mes:
                mes = date.today().month
            if not ano:
                ano = date.today().year
            
            # Primeiro e último dia do mês
            primeiro_dia = date(ano, mes, 1)
            if mes == 12:
                ultimo_dia = date(ano + 1, 1, 1)
            else:
                ultimo_dia = date(ano, mes + 1, 1)
            
            expenses = cls.get_user_expenses(db_session, user_id, primeiro_dia, ultimo_dia)
            return sum(float(expense.valor) for expense in expenses)
        except Exception as e:
            logger.error(f"Erro ao calcular total do mês: {e}")
            return 0
    
    def format_valor(self):
        """Formatar valor para exibição"""
        return f"R$ {float(self.valor):.2f}".replace('.', ',')