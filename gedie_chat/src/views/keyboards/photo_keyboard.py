"""
Teclados para funcionalidade de fotos
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class PhotoKeyboard:
    """Teclados relacionados à análise de fotos"""
    
    @staticmethod
    def get_confirmation_keyboard(analysis_result: dict):
        """Keyboard de confirmação da análise"""
        
        keyboard = []
        
        # Primeira linha - Confirmar
        keyboard.append([
            InlineKeyboardButton("✅ Confirmar Gasto", callback_data="photo:confirm")
        ])
        
        # Segunda linha - Edições
        edit_buttons = []
        if analysis_result.get('valor_total'):
            edit_buttons.append(
                InlineKeyboardButton("💰 Editar Valor", callback_data="photo:edit_value")
            )
        
        edit_buttons.append(
            InlineKeyboardButton("🏷️ Editar Categoria", callback_data="photo:edit_category")
        )
        
        keyboard.append(edit_buttons)
        
        # Terceira linha - Cancelar
        keyboard.append([
            InlineKeyboardButton("❌ Cancelar", callback_data="photo:cancel")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_photo_options():
        """Opções relacionadas a fotos no menu principal"""
        keyboard = [
            [
                InlineKeyboardButton("📷 Enviar Comprovante", callback_data="photo:guide"),
                InlineKeyboardButton("💰 Registro Manual", callback_data="expense:register")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)