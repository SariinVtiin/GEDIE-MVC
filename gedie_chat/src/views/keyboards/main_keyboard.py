"""
Teclados principais do bot - VERSÃO COM FOTOS
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class MainKeyboard:
    """Teclados do menu principal"""
    
    @staticmethod  
    def get_main_menu():
        """Menu principal"""
        keyboard = [
            [
                InlineKeyboardButton("📷 Enviar Comprovante", callback_data="photo:guide"),
                InlineKeyboardButton("💰 Registrar Gasto", callback_data="expense:register")
            ],
            [
                InlineKeyboardButton("💸 Ver Gastos", callback_data="expense:view_menu"),
                InlineKeyboardButton("🏷️ Categorias", callback_data="category:menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_back_to_main():
        """Voltar ao menu"""
        keyboard = [
            [InlineKeyboardButton("🔙 Menu Principal", callback_data="main:menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_confirm_cancel():
        """Botões de confirmação/cancelamento genéricos"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirmar", callback_data="confirm:yes"),
                InlineKeyboardButton("❌ Cancelar", callback_data="confirm:no")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_registration_options():
        """Opções de registro de gastos"""
        keyboard = [
            [
                InlineKeyboardButton("📷 Por Foto (IA)", callback_data="photo:guide"),
            ],
            [
                InlineKeyboardButton("💰 Manual", callback_data="expense:register"),
            ],
            [
                InlineKeyboardButton("🔙 Voltar", callback_data="main:menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

class ExpenseKeyboard:
    """Teclados relacionados a gastos"""
    
    @staticmethod
    def get_view_options():
        """Opções para visualizar gastos"""
        keyboard = [
            [
                InlineKeyboardButton("📅 Hoje", callback_data="expense:view:today"),
                InlineKeyboardButton("📆 Esta Semana", callback_data="expense:view:week")
            ],
            [
                InlineKeyboardButton("📊 Este Mês", callback_data="expense:view:month"),
                InlineKeyboardButton("🔍 Personalizado", callback_data="expense:view:custom")
            ],
            [
                InlineKeyboardButton("🔙 Voltar", callback_data="main:menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_expense_actions(expense_id: int):
        """Ações para um gasto específico"""
        keyboard = [
            [
                InlineKeyboardButton("✏️ Editar", callback_data=f"expense:edit:{expense_id}"),
                InlineKeyboardButton("🗑️ Excluir", callback_data=f"expense:delete:{expense_id}")
            ],
            [
                InlineKeyboardButton("🔙 Voltar", callback_data="expense:view_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_description_options():
        """Opções para adicionar descrição"""
        keyboard = [
            [
                InlineKeyboardButton("✏️ Adicionar Descrição", callback_data="expense:add_description"),
                InlineKeyboardButton("✅ Confirmar Sem Descrição", callback_data="expense:confirm")
            ],
            [
                InlineKeyboardButton("❌ Cancelar", callback_data="expense:cancel")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

class CategoryKeyboard:
    """Teclados de categorias"""
    
    @staticmethod
    def get_categories_grid(categories, action="select"):
        """Grid de categorias em formato de botões"""
        keyboard = []
        
        # Organizar categorias em linhas de 2
        for i in range(0, len(categories), 2):
            row = []
            for j in range(2):
                if i + j < len(categories):
                    cat = categories[i + j]
                    text = f"{cat.icone} {cat.nome}"
                    callback = f"category:{action}:{cat.id}"
                    row.append(InlineKeyboardButton(text, callback_data=callback))
            keyboard.append(row)
        
        # Botões adicionais baseados na ação
        if action == "select" or action == "expense_select":
            keyboard.append([
                InlineKeyboardButton("➕ Nova Categoria", callback_data="category:create")
            ])
        
        keyboard.append([
            InlineKeyboardButton("🔙 Voltar", callback_data="main:menu")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_category_menu():
        """Menu de gerenciamento de categorias"""
        keyboard = [
            [
                InlineKeyboardButton("📋 Minhas Categorias", callback_data="category:list"),
                InlineKeyboardButton("➕ Nova Categoria", callback_data="category:create")
            ],
            [
                InlineKeyboardButton("🔙 Menu Principal", callback_data="main:menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)