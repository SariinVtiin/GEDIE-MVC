"""
Controlador de configurações do usuário
"""

import random
from loguru import logger
from config.database_config import SessionLocal
from models.user_model import User
from views.keyboards.main_keyboard import SettingsKeyboard
from views.messages.settings_messages import SettingsMessages
from utils.state_manager import state_manager

class SettingsController:
    """Controlador para configurações do usuário"""
    
    async def handle_callback(self, query, parts):
        """Manipular callbacks de configurações"""
        if len(parts) < 2:
            return
        
        subaction = parts[1]
        user_id = query.from_user.id
        
        logger.info(f"Settings callback: {subaction} - User: {user_id}")
        
        if subaction == "menu":
            await self._show_settings_menu(query)
        elif subaction == "generate_code":
            await self._generate_access_code(query)
        elif subaction == "view_code":
            await self._view_current_code(query)
        elif subaction == "regenerate_code":
            await self._regenerate_access_code(query)
        elif subaction == "show_id":
            await self._show_user_id(query)
        elif subaction == "web_help":
            await self._show_web_help(query)
    
    async def _show_settings_menu(self, query):
        """Mostrar menu de configurações"""
        user_id = query.from_user.id
        
        try:
            # Buscar usuário para verificar se já tem código
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            db.close()
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                return
            
            has_code = user.codigo_acesso is not None
            
            message = SettingsMessages.settings_menu_message(user.nome, has_code)
            keyboard = SettingsKeyboard.get_settings_menu(has_code)
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao mostrar menu de configurações: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def _generate_access_code(self, query):
        """Gerar novo código de acesso"""
        user_id = query.from_user.id
        
        try:
            # Gerar código aleatório de 6 dígitos
            code = self._generate_random_code()
            
            # Salvar no banco
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                db.close()
                return
            
            # Atualizar código no banco
            success = User.update_access_code(db, user.id, code)
            db.close()
            
            if success:
                logger.info(f"✅ Código gerado para usuário {user_id}: {code}")
                
                message = SettingsMessages.code_generated_message(code)
                keyboard = SettingsKeyboard.get_code_actions()
                
                await query.edit_message_text(
                    message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text("❌ Erro ao salvar código.")
            
        except Exception as e:
            logger.error(f"Erro ao gerar código: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def _view_current_code(self, query):
        """Visualizar código atual"""
        user_id = query.from_user.id
        
        try:
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            db.close()
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                return
            
            if not user.codigo_acesso:
                message = SettingsMessages.no_code_message()
                keyboard = SettingsKeyboard.get_no_code_options()
            else:
                message = SettingsMessages.current_code_message(user.codigo_acesso)
                keyboard = SettingsKeyboard.get_code_actions()
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao visualizar código: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def _regenerate_access_code(self, query):
        """Regenerar código de acesso"""
        user_id = query.from_user.id
        
        try:
            # Gerar novo código
            new_code = self._generate_random_code()
            
            # Atualizar no banco
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                db.close()
                return
            
            success = User.update_access_code(db, user.id, new_code)
            db.close()
            
            if success:
                logger.info(f"✅ Código regenerado para usuário {user_id}: {new_code}")
                
                message = SettingsMessages.code_regenerated_message(new_code)
                keyboard = SettingsKeyboard.get_code_actions()
                
                await query.edit_message_text(
                    message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text("❌ Erro ao regenerar código.")
            
        except Exception as e:
            logger.error(f"Erro ao regenerar código: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def _show_user_id(self, query):
        """Mostrar ID do usuário"""
        user_id = query.from_user.id
        
        try:
            message = SettingsMessages.id_help_message(user_id)
            keyboard = SettingsKeyboard.get_web_help_options()
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao mostrar ID: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def _show_web_help(self, query):
        """Mostrar ajuda sobre versão web"""
        try:
            message = """🌐 **Versão Web do GEDIE**

🎯 **O que você pode fazer na web:**
• 📊 Ver gráficos detalhados de gastos
• 📈 Analisar relatórios por período
• 🗂️ Gerenciar categorias avançado
• 📱 Dashboard completo
• 💡 Insights inteligentes

🔐 **Como acessar:**
1. **Gere seu código** nas configurações
2. **Anote seu ID** do Telegram
3. **Acesse:** `http://localhost:5000`
4. **Faça login** com ID + código

✅ **Sincronização automática** com este bot!

**Precisa de ajuda?**"""
            
            keyboard = SettingsKeyboard.get_web_help_options()
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao mostrar ajuda web: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    def _generate_random_code(self):
        """Gerar código aleatório de 6 dígitos"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])