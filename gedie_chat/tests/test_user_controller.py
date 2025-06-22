import pytest
from controllers.user_controller import UserController
from models.user_model import User

@pytest.mark.asyncio
async def test_get_or_create_user(monkeypatch, _engine_and_session):
    _, TestSessionLocal = _engine_and_session
    monkeypatch.setattr("controllers.user_controller.SessionLocal", TestSessionLocal)

    uc = UserController()
    await uc.get_or_create_user(telegram_id=999, name="Tester")

    with TestSessionLocal() as s:
        reloaded = User.get_by_telegram_id(s, 999)
        assert reloaded.nome == "Tester"
