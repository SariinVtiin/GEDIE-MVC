"""
Testes unitários para os Models do GEDIE
Execute com: pytest test_models.py -v
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports dos models (ajustar conforme estrutura real do projeto)
# from models.expense_model import Expense
# from models.category_model import Category
# from models.user_model import User

# Como não temos os models reais, vamos criar versões simplificadas para teste
class Expense:
    def __init__(self, amount, description, category_id, user_id, date=None):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self.amount = Decimal(str(amount))
        self.description = description
        self.category_id = category_id
        self.user_id = user_id
        self.date = date or datetime.now()
        self.id = None
        self.status = "CONFIRMED"
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'description': self.description,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status
        }
    
    @staticmethod
    def total_by_period(expenses, period="month"):
        """Calcula total de despesas por período"""
        if period == "month":
            current_month = datetime.now().month
            current_year = datetime.now().year
            filtered = [e for e in expenses 
                       if e.date.month == current_month and e.date.year == current_year]
        elif period == "day":
            today = datetime.now().date()
            filtered = [e for e in expenses if e.date.date() == today]
        else:
            filtered = expenses
        
        return sum(e.amount for e in filtered)


class Category:
    def __init__(self, name, type="EXPENSE", icon="📦", user_id=None):
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty")
        self.name = name.strip()
        self.type = type
        self.icon = icon
        self.user_id = user_id
        self.id = None
        self.active = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'icon': self.icon,
            'active': self.active
        }


class User:
    def __init__(self, telegram_id, name, access_code=None):
        if not telegram_id:
            raise ValueError("Telegram ID is required")
        self.telegram_id = str(telegram_id)
        self.name = name
        self.access_code = access_code or self._generate_code()
        self.id = None
        self.active = True
    
    def _generate_code(self):
        """Gera código de 6 dígitos"""
        import random
        return str(random.randint(100000, 999999))
    
    def to_dict(self):
        return {
            'id': self.id,
            'telegram_id': self.telegram_id,
            'name': self.name,
            'access_code': self.access_code,
            'active': self.active
        }


# TESTES DOS MODELS

class TestExpenseModel:
    """Testes para o modelo Expense"""
    
    def test_create_valid_expense(self):
        """Testa criação de despesa válida"""
        expense = Expense(
            amount=50.00,
            description="Almoço",
            category_id=1,
            user_id=1
        )
        assert expense.amount == Decimal('50.00')
        assert expense.description == "Almoço"
        assert expense.status == "CONFIRMED"
    
    def test_expense_with_zero_amount_raises_error(self):
        """Testa que despesa com valor zero lança erro"""
        with pytest.raises(ValueError, match="Amount must be greater than 0"):
            Expense(amount=0, description="Test", category_id=1, user_id=1)
    
    def test_expense_with_negative_amount_raises_error(self):
        """Testa que despesa com valor negativo lança erro"""
        with pytest.raises(ValueError):
            Expense(amount=-10.50, description="Test", category_id=1, user_id=1)
    
    def test_expense_to_dict(self):
        """Testa serialização da despesa"""
        expense = Expense(
            amount=25.50,
            description="Uber",
            category_id=2,
            user_id=1
        )
        expense.id = 123
        
        result = expense.to_dict()
        
        assert result['id'] == 123
        assert result['amount'] == 25.50
        assert result['description'] == "Uber"
        assert result['category_id'] == 2
        assert result['status'] == "CONFIRMED"
        assert 'date' in result
    
    def test_total_by_period_month(self):
        """Testa cálculo de total por mês"""
        # Criar despesas do mês atual
        today = datetime.now()
        expenses = [
            Expense(100, "Despesa 1", 1, 1, date=today),
            Expense(50, "Despesa 2", 1, 1, date=today),
            Expense(25, "Despesa 3", 1, 1, date=today - timedelta(days=35))  # Mês passado
        ]
        
        total = Expense.total_by_period(expenses, "month")
        assert total == Decimal('150')  # Só as duas primeiras
    
    def test_total_by_period_day(self):
        """Testa cálculo de total por dia"""
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        expenses = [
            Expense(100, "Despesa hoje", 1, 1, date=today),
            Expense(50, "Despesa ontem", 1, 1, date=yesterday)
        ]
        
        total = Expense.total_by_period(expenses, "day")
        assert total == Decimal('100')  # Só a de hoje


class TestCategoryModel:
    """Testes para o modelo Category"""
    
    def test_create_valid_category(self):
        """Testa criação de categoria válida"""
        category = Category(name="Alimentação", icon="🍕", user_id=1)
        assert category.name == "Alimentação"
        assert category.icon == "🍕"
        assert category.type == "EXPENSE"
        assert category.active is True
    
    def test_category_name_is_trimmed(self):
        """Testa que nome da categoria é trimado"""
        category = Category(name="  Transporte  ", user_id=1)
        assert category.name == "Transporte"
    
    def test_empty_category_name_raises_error(self):
        """Testa que categoria sem nome lança erro"""
        with pytest.raises(ValueError, match="Category name cannot be empty"):
            Category(name="", user_id=1)
    
    def test_whitespace_category_name_raises_error(self):
        """Testa que categoria com apenas espaços lança erro"""
        with pytest.raises(ValueError):
            Category(name="   ", user_id=1)
    
    def test_category_to_dict(self):
        """Testa serialização da categoria"""
        category = Category(name="Saúde", icon="💊", user_id=1)
        category.id = 5
        
        result = category.to_dict()
        
        assert result['id'] == 5
        assert result['name'] == "Saúde"
        assert result['icon'] == "💊"
        assert result['type'] == "EXPENSE"
        assert result['active'] is True


class TestUserModel:
    """Testes para o modelo User"""
    
    def test_create_valid_user(self):
        """Testa criação de usuário válido"""
        user = User(telegram_id="123456789", name="João")
        assert user.telegram_id == "123456789"
        assert user.name == "João"
        assert user.active is True
        assert len(user.access_code) == 6
        assert user.access_code.isdigit()
    
    def test_user_with_custom_access_code(self):
        """Testa usuário com código de acesso customizado"""
        user = User(telegram_id="987654321", name="Maria", access_code="445376")
        assert user.access_code == "445376"
    
    def test_user_without_telegram_id_raises_error(self):
        """Testa que usuário sem telegram_id lança erro"""
        with pytest.raises(ValueError, match="Telegram ID is required"):
            User(telegram_id=None, name="Test")
    
    def test_user_to_dict(self):
        """Testa serialização do usuário"""
        user = User(telegram_id="123456789", name="Pedro", access_code="123456")
        user.id = 10
        
        result = user.to_dict()
        
        assert result['id'] == 10
        assert result['telegram_id'] == "123456789"
        assert result['name'] == "Pedro"
        assert result['access_code'] == "123456"
        assert result['active'] is True


# Fixtures para testes
@pytest.fixture
def sample_expense():
    """Fixture que retorna uma despesa de exemplo"""
    return Expense(
        amount=100.00,
        description="Compras no mercado",
        category_id=1,
        user_id=1
    )

@pytest.fixture
def sample_category():
    """Fixture que retorna uma categoria de exemplo"""
    return Category(name="Alimentação", icon="🍕", user_id=1)

@pytest.fixture
def sample_user():
    """Fixture que retorna um usuário de exemplo"""
    return User(telegram_id="123456789", name="Usuário Teste")


# Testes de integração entre models
class TestModelIntegration:
    """Testes de integração entre os models"""
    
    def test_expense_with_category_and_user(self, sample_category, sample_user):
        """Testa criação de despesa com categoria e usuário"""
        sample_category.id = 1
        sample_user.id = 1
        
        expense = Expense(
            amount=50.00,
            description="Jantar",
            category_id=sample_category.id,
            user_id=sample_user.id
        )
        
        assert expense.category_id == sample_category.id
        assert expense.user_id == sample_user.id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])