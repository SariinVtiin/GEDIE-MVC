"""
Controlador principal do bot - VERSÃO CORRIGIDA
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
from controllers.photo_controller import PhotoController

class BotController:
    """Controlador principal do bot"""
    
    def __init__(self):
        self.user_controller = UserController()
        self.expense_controller = ExpenseController()
        self.category_controller = CategoryController()
        self.photo_controller = PhotoController()  # ADICIONAR

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        try:
            user = update.effective_user
            telegram_id = user.id
            user_name = user.first_name or "Usuário"
            
            logger.info(f"Usuário {telegram_id} ({user_name}) iniciou o bot")
            
            # Registrar usuário
            db_user = await self.user_controller.get_or_create_user(telegram_id, user_name)
            
            if not db_user:
                await update.message.reply_text("❌ Erro interno. Tente novamente.")
                return
            
            # Limpar estado
            state_manager.clear_state(telegram_id)
            
            # Mensagem de boas-vindas
            message = f"""👋 Olá, **{user_name}**! Bem-vindo ao GEDIE!

🎯 **Gerencie seus gastos de forma inteligente**

Escolha uma opção para começar:"""
            
            keyboard = MainKeyboard.get_main_menu()
            
            await update.message.reply_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro no start: {e}")
            await update.message.reply_text("❌ Erro interno.")
    
    async def callback_router(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Roteador de callbacks"""
        try:
            query = update.callback_query
            await query.answer()
            
            callback_data = query.data
            user_id = update.effective_user.id
            
            logger.info(f"Callback {callback_data} do usuário {user_id}")
            
            parts = callback_data.split(":")
            action = parts[0]
            
            if action == "main":
                await self._handle_main_menu(query, parts)
            elif action == "expense":
                await self.expense_controller.handle_callback(query, parts)
            elif action == "category":
                await self.category_controller.handle_callback(query, parts)
            elif action == "photo":
                await self.photo_controller.handle_photo_callback(query, parts)
            elif action == "confirm":
                await self._handle_confirmation(query, parts)
            else:
                await query.edit_message_text("❌ Ação não reconhecida.")
        
        except Exception as e:
            logger.error(f"Erro no callback: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para mensagens"""
        try:
            user_id = update.effective_user.id
            message_text = update.message.text.strip()
            
            if state_manager.is_waiting_input(user_id):
                await self.expense_controller.handle_text_input(update, message_text)
            else:
                await update.message.reply_text(
                    "🤖 Use os botões abaixo para interagir!",
                    reply_markup=MainKeyboard.get_main_menu()
                )
        
        except Exception as e:
            logger.error(f"Erro no message handler: {e}")
            await update.message.reply_text("❌ Erro interno.")
    
    async def _handle_main_menu(self, query, parts):
        """Menu principal"""
        if len(parts) > 1 and parts[1] == "menu":
            state_manager.clear_state(query.from_user.id)
            
            message = "🏠 **Menu Principal**\n\nEscolha uma opção:"
            keyboard = MainKeyboard.get_main_menu()
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
    
    async def _handle_confirmation(self, query, parts):
        """Confirmações"""
        user_id = query.from_user.id
        
        if len(parts) > 1:
            if parts[1] == "yes":
                await self.expense_controller.confirm_pending_action(query)
            elif parts[1] == "no":
                state_manager.clear_state(user_id)
                await query.edit_message_text(
                    "❌ Ação cancelada.",
                    reply_markup=MainKeyboard.get_back_to_main()
                )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler de erros"""
        logger.error(f"Erro: {context.error}")
        
        try:
            if update.message:
                await update.message.reply_text("❌ Erro inesperado.")
            elif update.callback_query:
                await update.callback_query.edit_message_text("❌ Erro inesperado.")
        except:
            pass
    
    def get_handlers(self):
        """Retornar handlers"""
        return [
            CommandHandler("start", self.start_command),
            CallbackQueryHandler(self.callback_router),
            MessageHandler(filters.PHOTO, self.photo_controller.handle_photo),  # ADICIONAR
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler)
        ]