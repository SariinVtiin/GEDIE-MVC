import datetime
from models.user_model import User
from models.category_model import Category, TipoCategoria
from models.expense_model import Expense

def test_user_creation(db_session):
    user = User.create_user(db_session, telegram_id=1, nome="Alice")
    again = User.get_by_telegram_id(db_session, 1)
    assert again.nome == "Alice"

def test_default_categories(db_session):
    user = User.create_user(db_session, 2, "Bob")
    cats = Category.create_default_categories(db_session, user.id)
    assert len(cats) == 8
    assert all(c.user_id == user.id for c in cats)

def test_expense_crud(db_session):
    user = User.create_user(db_session, 3, "Carol")
    cat = Category(nome="Teste", icone="🧪", cor="#fff", user_id=user.id,
                   tipo=TipoCategoria.DESPESA).save(db_session)

    exp = Expense.create_expense(db_session, user.id, cat.id, 19.9, "Café")
    assert float(exp.valor) == 19.9          # Decimal → float

    today = datetime.date.today()
    expenses = Expense.get_user_expenses(db_session, user.id, today, today)
    assert len(expenses) == 1

    total_mes = Expense.get_month_total(db_session, user.id, today.month, today.year)
    assert total_mes == 19.9
