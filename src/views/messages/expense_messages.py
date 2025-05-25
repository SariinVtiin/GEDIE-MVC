"""
Formatadores de mensagens para gastos - VERSÃO CORRIGIDA
"""

from typing import List, Dict, Any
from datetime import date, datetime
from models.expense_model import Expense
from models.category_model import Category

class ExpenseMessages:
    """Formatador de mensagens de gastos"""
    
    @staticmethod
    def expenses_list_message_from_data(expenses_data: List[Dict[str, Any]], period_title: str) -> str:
        """Lista de gastos formatada - VERSÃO SEGURA usando dados carregados"""
        if not expenses_data:
            return f"""📊 **{period_title}**

😴 Nenhum gasto registrado neste período.

Que tal começar a registrar seus gastos?"""
        
        total = sum(expense_data['valor'] for expense_data in expenses_data)
        total_formatado = f"R$ {total:.2f}".replace('.', ',')
        
        message = f"""📊 **{period_title}**

💰 **Total: {total_formatado}**
📝 **{len(expenses_data)} gasto{'s' if len(expenses_data) > 1 else ''}**

"""
        
        for expense_data in expenses_data[:10]:  # Mostrar até 10 gastos
            valor_formatado = f"R$ {expense_data['valor']:.2f}".replace('.', ',')
            data_formatada = expense_data['data_gasto'].strftime('%d/%m')
            
            message += f"• {expense_data['category_icone']} **{valor_formatado}** - {expense_data['category_nome']}"
            if expense_data.get('descricao'):
                descricao = expense_data['descricao']
                message += f" _{descricao[:30]}{'...' if len(descricao) > 30 else ''}_"
            message += f" ({data_formatada})\n"
        
        if len(expenses_data) > 10:
            message += f"\n_... e mais {len(expenses_data) - 10} gastos_"
        
        return message
    
    @staticmethod
    def welcome_message(user_name: str) -> str:
        """Mensagem de boas-vindas"""
        return f"""👋 Olá, **{user_name}**! Bem-vindo ao GEDIE!

🎯 **Gerencie seus gastos de forma simples e organizada**

Escolha uma opção abaixo para começar:"""
    
    @staticmethod
    def select_category_message() -> str:
        """Mensagem para seleção de categoria"""
        return """💰 **Registrar novo gasto**

🏷️ Selecione a categoria do seu gasto:"""
    
    @staticmethod
    def enter_amount_message(category_name: str, category_icon: str) -> str:
        """Mensagem para inserir valor"""
        return f"""💵 **Valor do gasto**

{category_icon} Categoria: **{category_name}**

Digite o valor gasto (apenas números):
*Exemplo: 25.50 ou 25,50*"""
    
    @staticmethod
    def confirm_expense_message(valor: float, category_name: str, category_icon: str) -> str:
        """Mensagem de confirmação do gasto"""
        valor_formatado = f"R$ {valor:.2f}".replace('.', ',')
        return f"""✅ **Confirmar gasto**

💰 Valor: **{valor_formatado}**
{category_icon} Categoria: **{category_name}**
📅 Data: **{date.today().strftime('%d/%m/%Y')}**

Deseja adicionar uma descrição ou confirmar o gasto?"""
    
    @staticmethod
    def enter_description_message() -> str:
        """Mensagem para inserir descrição"""
        return """📝 **Descrição do gasto**

Digite uma descrição para o gasto (opcional):
*Exemplo: Almoço no restaurante X*"""
    
    @staticmethod
    def expense_saved_message(expense: Expense) -> str:
        """Mensagem de gasto salvo - VERSÃO ORIGINAL (pode dar erro de sessão)"""
        valor_formatado = f"R$ {float(expense.valor):.2f}".replace('.', ',')
        return f"""🎉 **Gasto registrado com sucesso!**

💰 Valor: **{valor_formatado}**
{expense.category.icone} Categoria: **{expense.category.nome}**
📅 Data: **{expense.data_gasto.strftime('%d/%m/%Y')}**
{f'📝 Descrição: **{expense.descricao}**' if expense.descricao else ''}

✅ Seu gasto foi salvo e já está nos seus relatórios!"""
    
    @staticmethod
    def expense_saved_message_from_data(expense_data: Dict[str, Any]) -> str:
        """Mensagem de gasto salvo - VERSÃO SEGURA usando dados carregados"""
        valor_formatado = f"R$ {expense_data['valor']:.2f}".replace('.', ',')
        data_formatada = expense_data['data_gasto'].strftime('%d/%m/%Y')
        
        message = f"""🎉 **Gasto registrado com sucesso!**

💰 Valor: **{valor_formatado}**
{expense_data['category_icone']} Categoria: **{expense_data['category_nome']}**
📅 Data: **{data_formatada}**"""
        
        if expense_data.get('descricao'):
            message += f"\n📝 Descrição: **{expense_data['descricao']}**"
        
        message += "\n\n✅ Seu gasto foi salvo e já está nos seus relatórios!"
        
        return message
    
    @staticmethod
    def expenses_list_message(expenses: List[Expense], period_title: str) -> str:
        """Lista de gastos formatada"""
        if not expenses:
            return f"""📊 **{period_title}**

😴 Nenhum gasto registrado neste período.

Que tal começar a registrar seus gastos?"""
        
        total = sum(float(expense.valor) for expense in expenses)
        total_formatado = f"R$ {total:.2f}".replace('.', ',')
        
        message = f"""📊 **{period_title}**

💰 **Total: {total_formatado}**
📝 **{len(expenses)} gasto{'s' if len(expenses) > 1 else ''}**

"""
        
        for expense in expenses[:10]:  # Mostrar até 10 gastos
            valor_formatado = f"R$ {float(expense.valor):.2f}".replace('.', ',')
            data_formatada = expense.data_gasto.strftime('%d/%m')
            
            message += f"• {expense.category.icone} **{valor_formatado}** - {expense.category.nome}"
            if expense.descricao:
                message += f" _{expense.descricao[:30]}{'...' if len(expense.descricao) > 30 else ''}_"
            message += f" ({data_formatada})\n"
        
        if len(expenses) > 10:
            message += f"\n_... e mais {len(expenses) - 10} gastos_"
        
        return message
    
    @staticmethod
    def invalid_amount_message() -> str:
        """Mensagem de valor inválido"""
        return """❌ **Valor inválido**

Por favor, digite apenas números para o valor.

✅ **Exemplos válidos:**
• 25.50
• 25,50  
• 100
• 12.99

Digite novamente o valor:"""
    
    @staticmethod
    def expense_cancelled_message() -> str:
        """Mensagem de gasto cancelado"""
        return """❌ **Gasto cancelado**

Nenhum gasto foi registrado. Você pode tentar novamente quando quiser!"""