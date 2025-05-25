"""
Controlador de categorias - VERSÃO CORRIGIDA
"""

from loguru import logger
from config.database_config import SessionLocal
from models.category_model import Category
from models.user_model import User
from views.keyboards.main_keyboard import CategoryKeyboard
from utils.state_manager import state_manager, ConversationState

class CategoryController:
    """Controlador de categorias"""
    
    def _debug_user_state(self, user_id, action=""):
        """Debug do estado do usuário"""
        state = state_manager.get_state(user_id)
        data = state_manager.get_data(user_id)
        logger.info(f"🔍 CATEGORY DEBUG {action} - User: {user_id}")
        logger.info(f"    Estado: {state}")
        logger.info(f"    Dados: {data}")
    
    async def handle_callback(self, query, parts):
        """Manipular callbacks de categorias"""
        if len(parts) < 2:
            return
        
        subaction = parts[1]
        user_id = query.from_user.id
        
        logger.info(f"Category callback: {subaction} - User: {user_id}")
        self._debug_user_state(user_id, f"CALLBACK {subaction}")
        
        if subaction == "expense_select":
            # Seleção de categoria para gasto
            if len(parts) > 2:
                category_id = int(parts[2])
                await self._select_category_for_expense(query, category_id)
        elif subaction == "menu":
            await self._show_category_menu(query)
        elif subaction == "list":
            await self._list_categories(query)
    
    async def _select_category_for_expense(self, query, category_id):
        """Selecionar categoria para registro de gasto"""
        user_id = query.from_user.id
        
        try:
            logger.info(f"Selecionando categoria {category_id} para usuário {user_id}")
            
            # Buscar categoria
            db = SessionLocal()
            category = db.query(Category).filter(Category.id == category_id).first()
            
            if not category:
                logger.error(f"Categoria {category_id} não encontrada")
                await query.edit_message_text("❌ Categoria não encontrada.")
                db.close()
                return
            
            logger.info(f"Categoria encontrada: {category.nome} ({category.icone})")
            
            # Verificar se categoria pertence ao usuário
            user = User.get_by_telegram_id(db, user_id)
            if not user or category.user_id != user.id:
                logger.error(f"Categoria {category_id} não pertence ao usuário {user_id}")
                await query.edit_message_text("❌ Categoria inválida.")
                db.close()
                return
            
            db.close()
            
            # IMPORTANTE: Preservar dados existentes ao definir novo estado
            current_data = state_manager.get_data(user_id)
            logger.info(f"Dados existentes antes de salvar categoria: {current_data}")
            
            # Adicionar category_id aos dados existentes
            state_manager.set_state(
                user_id, 
                ConversationState.WAITING_AMOUNT,
                {'category_id': category_id}  # Dados novos serão mesclados com existentes
            )
            
            # Verificar se dados foram salvos corretamente
            updated_data = state_manager.get_data(user_id)
            logger.info(f"Dados após salvar categoria: {updated_data}")
            
            if updated_data.get('category_id') != category_id:
                logger.error(f"ERRO: category_id não foi salvo corretamente!")
                logger.error(f"Esperado: {category_id}, Obtido: {updated_data.get('category_id')}")
                await query.edit_message_text("❌ Erro interno. Tente novamente.")
                return
            
            self._debug_user_state(user_id, "APÓS SELECIONAR CATEGORIA")
            
            from views.messages.expense_messages import ExpenseMessages
            message = ExpenseMessages.enter_amount_message(category.nome, category.icone)
            
            await query.edit_message_text(message, parse_mode='Markdown')
            
            logger.info(f"✅ Categoria {category_id} selecionada com sucesso para usuário {user_id}")
            
        except Exception as e:
            logger.error(f"Erro ao selecionar categoria: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def _show_category_menu(self, query):
        """Mostrar menu de categorias"""
        message = "🏷️ **Gerenciar Categorias**\n\nEscolha uma opção:"
        keyboard = CategoryKeyboard.get_category_menu()
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    
    async def _list_categories(self, query):
        """Listar categorias do usuário"""
        user_id = query.from_user.id
        
        try:
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                db.close()
                return
            
            categories = Category.get_user_categories(db, user.id)
            db.close()
            
            if not categories:
                message = "😴 Você não possui categorias cadastradas."
            else:
                message = f"🏷️ **Suas Categorias** ({len(categories)})\n\n"
                for cat in categories:
                    message += f"• {cat.icone} **{cat.nome}** (ID: {cat.id})\n"
            
            keyboard = CategoryKeyboard.get_category_menu()
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao listar categorias: {e}")
            await query.edit_message_text("❌ Erro interno.")