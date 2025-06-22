import pytest
from controllers.expense_controller import ExpenseController
from utils.state_manager import state_manager, ConversationState
from models.user_model import User
from models.category_model import Category, TipoCategoria

@pytest.fixture
def controller(monkeypatch, _engine_and_session):
    _, TestSessionLocal = _engine_and_session
    monkeypatch.setattr("controllers.expense_controller.SessionLocal", TestSessionLocal)
    return ExpenseController()

@pytest.mark.asyncio
async def test_amount_validation(controller, db_session):
    uid = 1001

    # cria user + categoria
    user = User.create_user(db_session, uid, "Dave")
    cat = Category(nome="Foo", icone="💰", cor="#000", user_id=user.id,
                   tipo=TipoCategoria.DESPESA).save(db_session)

    # simula estado previamente escolhido
    state_manager.set_state(uid, ConversationState.WAITING_AMOUNT,
                            {"category_id": cat.id})

    # stub de Update simplificado
    class DummyMsg:
        text = ""
        async def reply_text(self, *_, **__):
            return None

    class DummyUpdate:
        effective_user = type("U", (), {"id": uid})
        message = DummyMsg()

    update = DummyUpdate()
    await controller._process_amount_input(update, "R$ 123,45")

    data = state_manager.get_data(uid)
    assert data["amount"] == 123.45
    assert state_manager.get_state(uid) == ConversationState.CONFIRMING_EXPENSE
