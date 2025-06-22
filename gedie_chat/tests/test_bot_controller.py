# tests/test_bot_start_ok.py
import pytest
from controllers.bot_controller import BotController
from utils.state_manager import state_manager, ConversationState

class DummyMessage:
    def __init__(self):
        self.text_sent = ""
    async def reply_text(self, text, **_):
        self.text_sent = text

class DummyUpdate:
    def __init__(self, uid, first_name="Tester"):
        self.effective_user = type("U", (), {"id": uid, "first_name": first_name})
        self.message = DummyMessage()

@pytest.mark.asyncio
async def test_start_creates_user(monkeypatch, _engine_and_session):
    _, Sess = _engine_and_session
    # forçar SessionLocal usado pelo controller
    monkeypatch.setattr("controllers.user_controller.SessionLocal", Sess)

    bot = BotController()
    up = DummyUpdate(42)

    await bot.start_command(up, None)

    assert "Bem-vindo ao GEDIE" in up.message.text_sent
    # garante que estado foi limpo
    assert state_manager.get_state(42) == ConversationState.IDLE
