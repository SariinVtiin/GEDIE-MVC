"""
Controlador principal do bot
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from loguru import logger

from controllers.user_controller import UserController
from controllers.expense_controller import ExpenseController
from controllers.category_controller import CategoryController
from views.keyboards.main_keyboard import MainKeyboard
from views.messages.expense_messages import ExpenseMessages
from utils.state_manager import state_manager, ConversationState

class BotController:
    """Controlador principal do bot"""
    
    def __init__(self):
        self.user_controller = UserController()
        self.expense_controller = ExpenseController()
        self.category_controller = CategoryController()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        try:
            user = update.effective_user
            telegram_id = user.id
            user_name = user.first_name or "Usuário"
            
            logger.info(f"Usuário {telegram_id} ({user_name}) iniciou o bot")
            
            # Registrar/buscar usuário
            db_user = await self.user_controller.get_or_create_user(
                telegram_id, user_name
            )
            
            if not db_user:
                await update.message.reply_text(
                    "❌ Erro interno. Tente novamente em alguns instantes."
                )
                return
            
            # Limpar estado e mostrar menu principal
            state_manager.clear_state(telegram_id)
            
            message = ExpenseMessages.welcome_message(user_name)
            keyboard = MainKeyboard.get_main_menu()
            
            await update.message.reply_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro no comando start: {e}")
            await update.message.reply_text(
                "❌ Erro interno. Tente novamente."
            )
    
    async def callback_router(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Roteador de callbacks dos botões"""
        try:
            query = update.callback_query
            await query.answer()
            
            callback_data = query.data
            user_id = update.effective_user.id
            
            logger.info(f"Callback {callback_data} do usuário {user_id}")
            
            # Parsear callback data: "acao:subacao:parametro"
            parts = callback_data.split(":")
            action = parts[0]
            
            # Roteamento baseado na ação
            if action == "main":
                await self._handle_main_menu(query, parts)
            elif action == "expense":
                await self.expense_controller.handle_callback(query, parts)
            elif action == "category":
                await self.category_controller.handle_callback(query, parts)
            elif action == "confirm":
                await self._handle_confirmation(query, parts)
            else:
                logger.warning(f"Ação desconhecida: {action}")
                await query.edit_message_text("❌ Ação não reconhecida.")
        
        except Exception as e:
            logger.error(f"Erro no callback router: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para mensagens de texto"""
        try:
            user_id = update.effective_user.id
            message_text = update.message.text.strip()
            
            logger.info(f"Mensagem de {user_id}: {message_text}")
            
            # Verificar se usuário está em um fluxo que espera input
            if state_manager.is_waiting_input(user_id):
                await self.expense_controller.handle_text_input(update, message_text)
            else:
                # Usuário enviou mensagem fora de contexto
                await update.message.reply_text(
                    "🤖 Use os botões abaixo para interagir comigo!",
                    reply_markup=MainKeyboard.get_main_menu()
                )
        
        except Exception as e:
            logger.error(f"Erro no message handler: {e}")
            await update.message.reply_text("❌ Erro interno.")
    
    async def _handle_main_menu(self, query, parts):
        """Manipular ações do menu principal"""
        if len(parts) > 1 and parts[1] == "menu":
            # Mostrar menu principal
            state_manager.clear_state(query.from_user.id)
            
            message = "🏠 **Menu Principal**\n\nEscolha uma opção:"
            keyboard = MainKeyboard.get_main_menu()
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
    
    async def _handle_confirmation(self, query, parts):
        """Manipular confirmações gerais"""
        user_id = query.from_user.id
        
        if len(parts) > 1:
            if parts[1] == "yes":
                # Confirmar ação pendente
                await self.expense_controller.confirm_pending_action(query)
            elif parts[1] == "no":
                # Cancelar ação
                state_manager.clear_state(user_id)
                await query.edit_message_text(
                    "❌ Ação cancelada.",
                    reply_markup=MainKeyboard.get_back_to_main()
                )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler de erros gerais"""
        logger.error(f"Erro não capturado: {context.error}")
        
        if update.message:
            await update.message.reply_text(
                "❌ Ocorreu um erro inesperado. Tente novamente."
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                "❌ Ocorreu um erro inesperado. Tente novamente."
            )
    
    def get_handlers(self):
        """Retornar handlers para registrar no bot"""
        return [
            CommandHandler("start", self.start_command),
            CallbackQueryHandler(self.callback_router),
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler)
        ]