"""
Testes unitários para Controllers/Services do GEDIE
Execute com: pytest test_controllers.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import json

# Controllers simulados para teste
class ExpenseController:
    def __init__(self, db=None):
        self.db = db or Mock()
    
    def create_expense(self, user_id, amount, description, category_id, source="manual"):
        """Cria uma nova despesa"""
        # Validações
        if amount <= 0:
            return {"error": "Amount must be greater than 0"}, 400
        
        # Verificar se categoria existe
        category = self.db.get_category(category_id)
        if not category:
            return {"error": "Category not found"}, 404
        
        # Verificar se categoria pertence ao usuário
        if category.get('user_id') != user_id:
            return {"error": "Unauthorized"}, 403
        
        # Criar despesa
        expense = {
            'user_id': user_id,
            'amount': amount,
            'description': description,
            'category_id': category_id,
            'status': 'PENDING' if source == 'photo' else 'CONFIRMED',
            'created_at': datetime.now()
        }
        
        result = self.db.insert_expense(expense)
        return result, 201
    
    def get_expenses_by_period(self, user_id, period="month"):
        """Retorna despesas por período"""
        expenses = self.db.get_user_expenses(user_id, period)
        total = sum(e.get('amount', 0) for e in expenses)
        
        return {
            'expenses': expenses,
            'total': total,
            'period': period
        }
    
    def delete_expense(self, user_id, expense_id):
        """Deleta uma despesa"""
        expense = self.db.get_expense(expense_id)
        
        if not expense:
            return {"error": "Expense not found"}, 404
        
        if expense.get('user_id') != user_id:
            return {"error": "Unauthorized"}, 403
        
        self.db.delete_expense(expense_id)
        return {"status": "success"}, 200


class CategoryController:
    def __init__(self, db=None):
        self.db = db or Mock()
    
    def create_category(self, user_id, name, icon="📦"):
        """Cria nova categoria"""
        if not name or not name.strip():
            return {"error": "Category name is required"}, 400
        
        # Verificar se já existe
        existing = self.db.get_category_by_name(user_id, name)
        if existing:
            return {"error": "Category already exists"}, 409
        
        category = {
            'user_id': user_id,
            'name': name.strip(),
            'icon': icon,
            'active': True
        }
        
        result = self.db.insert_category(category)
        return result, 201
    
    def delete_category(self, user_id, category_id):
        """Deleta categoria se não estiver em uso"""
        category = self.db.get_category(category_id)
        
        if not category:
            return {"error": "Category not found"}, 404
        
        if category.get('user_id') != user_id:
            return {"error": "Unauthorized"}, 403
        
        # Verificar se está em uso
        expenses_count = self.db.count_expenses_by_category(category_id)
        if expenses_count > 0:
            return {"error": f"Category is used in {expenses_count} expenses"}, 400
        
        self.db.delete_category(category_id)
        return {"status": "success"}, 200


# TESTES DOS CONTROLLERS

class TestExpenseController:
    """Testes para ExpenseController"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock do banco de dados"""
        return Mock()
    
    @pytest.fixture
    def controller(self, mock_db):
        """Controller com mock do DB"""
        return ExpenseController(db=mock_db)
    
    def test_create_expense_success(self, controller, mock_db):
        """Testa criação de despesa com sucesso"""
        # Setup
        mock_db.get_category.return_value = {'id': 1, 'user_id': 10}
        mock_db.insert_expense.return_value = {'id': 123, 'status': 'CONFIRMED'}
        
        # Execute
        result, status = controller.create_expense(
            user_id=10,
            amount=50.00,
            description="Almoço",
            category_id=1
        )
        
        # Assert
        assert status == 201
        assert result['status'] == 'CONFIRMED'
        mock_db.insert_expense.assert_called_once()
    
    def test_create_expense_with_photo_source(self, controller, mock_db):
        """Testa que despesa de foto fica como PENDING"""
        mock_db.get_category.return_value = {'id': 1, 'user_id': 10}
        mock_db.insert_expense.return_value = {'id': 124, 'status': 'PENDING'}
        
        result, status = controller.create_expense(
            user_id=10,
            amount=25.00,
            description="Cupom",
            category_id=1,
            source="photo"
        )
        
        assert status == 201
        # Verificar que foi passado PENDING
        call_args = mock_db.insert_expense.call_args[0][0]
        assert call_args['status'] == 'PENDING'
    
    def test_create_expense_invalid_amount(self, controller):
        """Testa erro com valor inválido"""
        result, status = controller.create_expense(
            user_id=10,
            amount=0,
            description="Test",
            category_id=1
        )
        
        assert status == 400
        assert "Amount must be greater than 0" in result['error']
    
    def test_create_expense_category_not_found(self, controller, mock_db):
        """Testa erro quando categoria não existe"""
        mock_db.get_category.return_value = None
        
        result, status = controller.create_expense(
            user_id=10,
            amount=50.00,
            description="Test",
            category_id=999
        )
        
        assert status == 404
        assert "Category not found" in result['error']
    
    def test_create_expense_unauthorized_category(self, controller, mock_db):
        """Testa erro quando categoria é de outro usuário"""
        mock_db.get_category.return_value = {'id': 1, 'user_id': 99}  # Outro user
        
        result, status = controller.create_expense(
            user_id=10,
            amount=50.00,
            description="Test",
            category_id=1
        )
        
        assert status == 403
        assert "Unauthorized" in result['error']
    
    def test_get_expenses_by_period(self, controller, mock_db):
        """Testa busca de despesas por período"""
        mock_expenses = [
            {'id': 1, 'amount': 100.00},
            {'id': 2, 'amount': 50.00},
            {'id': 3, 'amount': 25.00}
        ]
        mock_db.get_user_expenses.return_value = mock_expenses
        
        result = controller.get_expenses_by_period(user_id=10, period="month")
        
        assert result['total'] == 175.00
        assert len(result['expenses']) == 3
        assert result['period'] == "month"
    
    def test_delete_expense_not_found(self, controller, mock_db):
        """Testa erro ao deletar despesa inexistente"""
        mock_db.get_expense.return_value = None
        
        result, status = controller.delete_expense(user_id=10, expense_id=999)
        
        assert status == 404
        assert "Expense not found" in result['error']
    
    def test_delete_expense_unauthorized(self, controller, mock_db):
        """Testa erro ao deletar despesa de outro usuário"""
        mock_db.get_expense.return_value = {'id': 1, 'user_id': 99}
        
        result, status = controller.delete_expense(user_id=10, expense_id=1)
        
        assert status == 403
        assert "Unauthorized" in result['error']


class TestCategoryController:
    """Testes para CategoryController"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock()
    
    @pytest.fixture
    def controller(self, mock_db):
        return CategoryController(db=mock_db)
    
    def test_create_category_success(self, controller, mock_db):
        """Testa criação de categoria com sucesso"""
        mock_db.get_category_by_name.return_value = None
        mock_db.insert_category.return_value = {'id': 5, 'name': 'Lazer'}
        
        result, status = controller.create_category(
            user_id=10,
            name="Lazer",
            icon="🎮"
        )
        
        assert status == 201
        assert result['name'] == 'Lazer'
    
    def test_create_category_empty_name(self, controller):
        """Testa erro com nome vazio"""
        result, status = controller.create_category(
            user_id=10,
            name="",
            icon="📦"
        )
        
        assert status == 400
        assert "Category name is required" in result['error']
    
    def test_create_category_already_exists(self, controller, mock_db):
        """Testa erro quando categoria já existe"""
        mock_db.get_category_by_name.return_value = {'id': 1, 'name': 'Alimentação'}
        
        result, status = controller.create_category(
            user_id=10,
            name="Alimentação",
            icon="🍕"
        )
        
        assert status == 409
        assert "Category already exists" in result['error']
    
    def test_delete_category_with_expenses(self, controller, mock_db):
        """Testa erro ao deletar categoria em uso"""
        mock_db.get_category.return_value = {'id': 1, 'user_id': 10}
        mock_db.count_expenses_by_category.return_value = 5
        
        result, status = controller.delete_category(user_id=10, category_id=1)
        
        assert status == 400
        assert "Category is used in 5 expenses" in result['error']
    
    def test_delete_category_success(self, controller, mock_db):
        """Testa deleção de categoria com sucesso"""
        mock_db.get_category.return_value = {'id': 1, 'user_id': 10}
        mock_db.count_expenses_by_category.return_value = 0
        
        result, status = controller.delete_category(user_id=10, category_id=1)
        
        assert status == 200
        assert result['status'] == 'success'
        mock_db.delete_category.assert_called_once_with(1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])