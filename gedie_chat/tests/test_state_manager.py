# tests/test_state_manager.py
from utils.state_manager import state_manager, ConversationState

def test_state_preservation():
    uid = 123
    state_manager.set_state(uid, ConversationState.WAITING_AMOUNT, {"category_id": 1})
    state_manager.update_data(uid, "amount", 100)
    data = state_manager.get_data(uid)

    assert data == {"category_id": 1, "amount": 100}
    assert state_manager.get_state(uid) == ConversationState.WAITING_AMOUNT

def test_clear_state():
    uid = 777
    state_manager.set_state(uid, ConversationState.IDLE, {})
    state_manager.clear_state(uid)
    assert state_manager.get_state(uid) == ConversationState.IDLE
    assert state_manager.get_data(uid) == {}
