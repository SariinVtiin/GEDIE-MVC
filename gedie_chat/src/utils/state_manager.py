"""
Gerenciador de estados da conversa - VERSÃO CORRIGIDA
"""

from enum import Enum
from typing import Dict, Any, Optional
from loguru import logger

class ConversationState(Enum):
    """Estados possíveis da conversa"""
    IDLE = "idle"
    WAITING_AMOUNT = "waiting_amount"
    WAITING_DESCRIPTION = "waiting_description"
    WAITING_CATEGORY_NAME = "waiting_category_name"
    CONFIRMING_EXPENSE = "confirming_expense"
    SELECTING_CATEGORY = "selecting_category"

class StateManager:
    """Gerenciador de estados dos usuários"""
    
    def __init__(self):
        # Armazenar estados em memória {user_id: {'state': state, 'data': {}}}
        self._user_states: Dict[int, Dict[str, Any]] = {}
    
    def set_state(self, user_id: int, state: ConversationState, data: Dict[str, Any] = None):
        """Definir estado do usuário PRESERVANDO dados existentes"""
        
        # Se já existe estado, preservar dados existentes
        current_data = {}
        if user_id in self._user_states:
            current_data = self._user_states[user_id].get('data', {})
        
        # Mesclar dados novos com existentes
        if data:
            current_data.update(data)
        
        self._user_states[user_id] = {
            'state': state,
            'data': current_data
        }
        
        logger.debug(f"Estado do usuário {user_id}: {state.value}")
        logger.debug(f"Dados preservados: {current_data}")
    
    def get_state(self, user_id: int) -> ConversationState:
        """Obter estado atual do usuário"""
        user_state = self._user_states.get(user_id, {})
        return user_state.get('state', ConversationState.IDLE)
    
    def get_data(self, user_id: int) -> Dict[str, Any]:
        """Obter dados do estado atual"""
        user_state = self._user_states.get(user_id, {})
        return user_state.get('data', {})
    
    def update_data(self, user_id: int, key: str, value: Any):
        """Atualizar dados do estado PRESERVANDO existentes"""
        if user_id not in self._user_states:
            self._user_states[user_id] = {
                'state': ConversationState.IDLE, 
                'data': {}
            }
        
        # Preservar dados existentes
        current_data = self._user_states[user_id]['data']
        current_data[key] = value
        
        logger.debug(f"Dados atualizados para usuário {user_id}: {key}={value}")
        logger.debug(f"Dados completos: {current_data}")
    
    def clear_state(self, user_id: int):
        """Limpar estado do usuário"""
        if user_id in self._user_states:
            del self._user_states[user_id]
        logger.debug(f"Estado do usuário {user_id} limpo")
    
    def is_waiting_input(self, user_id: int) -> bool:
        """Verificar se usuário está esperando input"""
        state = self.get_state(user_id)
        return state in [
            ConversationState.WAITING_AMOUNT,
            ConversationState.WAITING_DESCRIPTION,
            ConversationState.WAITING_CATEGORY_NAME
        ]
    
    def debug_user(self, user_id: int) -> str:
        """Debug completo de um usuário"""
        if user_id not in self._user_states:
            return f"Usuário {user_id} não possui estado ativo"
        
        user_data = self._user_states[user_id]
        return f"Usuário {user_id}: Estado={user_data['state'].value}, Dados={user_data['data']}"
    
    def list_all_states(self) -> Dict[int, str]:
        """Listar todos os estados ativos"""
        result = {}
        for user_id, state_data in self._user_states.items():
            result[user_id] = f"{state_data['state'].value} - {state_data['data']}"
        return result

# Instância global do gerenciador
state_manager = StateManager()