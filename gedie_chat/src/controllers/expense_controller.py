"""
Controlador de gastos - VERSÃO CORRIGIDA COM DEBUG
"""

import re
from datetime import date, datetime, timedelta
from typing import List, Optional
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger

from config.database_config import SessionLocal
from models.expense_model import Expense
from models.category_model import Category
from models.user_model import User
from views.keyboards.main_keyboard import MainKeyboard, ExpenseKeyboard, CategoryKeyboard
from views.messages.expense_messages import ExpenseMessages
from utils.state_manager import state_manager, ConversationState
from controllers.user_controller import UserController

class ExpenseController:
    """Controlador de gastos"""
    
    def __init__(self):
        self.user_controller = UserController()
    
    def _debug_user_state(self, user_id, action=""):
        """Debug do estado do usuário"""
        state = state_manager.get_state(user_id)
        data = state_manager.get_data(user_id)
        logger.info(f"🔍 DEBUG {action} - User: {user_id}")
        logger.info(f"    Estado: {state}")
        logger.info(f"    Dados: {data}")
    
    async def handle_callback(self, query, parts):
        """Manipular callbacks relacionados a gastos"""
        user_id = query.from_user.id
        
        if len(parts) < 2:
            return
        
        subaction = parts[1]
        
        self._debug_user_state(user_id, f"CALLBACK {subaction}")
        
        if subaction == "register":
            await self._start_expense_registration(query)
        elif subaction == "view_menu":
            await self._show_view_menu(query)
        elif subaction == "view":
            if len(parts) > 2:
                period = parts[2]
                await self._show_expenses_by_period(query, period)
        elif subaction == "confirm":
            await self._confirm_expense_callback(query)
        elif subaction == "cancel":
            await self._cancel_expense(query)
        elif subaction == "add_description":
            await self._request_description(query)
    
    async def _start_expense_registration(self, query):
        """Iniciar processo de registro de gasto"""
        user_id = query.from_user.id
        
        try:
            logger.info(f"Iniciando registro de gasto para usuário {user_id}")
            
            # Limpar estado anterior
            state_manager.clear_state(user_id)
            
            # Buscar usuário e suas categorias
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                db.close()
                return
            
            categories = Category.get_user_categories(db, user.id)
            db.close()
            
            if not categories:
                await query.edit_message_text(
                    "❌ Você não possui categorias cadastradas.",
                    reply_markup=MainKeyboard.get_back_to_main()
                )
                return
            
            # Definir estado e mostrar categorias
            state_manager.set_state(user_id, ConversationState.SELECTING_CATEGORY)
            
            self._debug_user_state(user_id, "APÓS DEFINIR SELECTING_CATEGORY")
            
            message = ExpenseMessages.select_category_message()
            keyboard = CategoryKeyboard.get_categories_grid(categories, "expense_select")
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao iniciar registro de gasto: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def _show_view_menu(self, query):
        """Mostrar menu de visualização de gastos"""
        message = "💸 **Ver Gastos**\n\nEscolha o período:"
        keyboard = ExpenseKeyboard.get_view_options()
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    
    async def _show_expenses_by_period(self, query, period):
        """Mostrar gastos por período"""
        user_id = query.from_user.id
        
        try:
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                db.close()
                return
            
            # Definir período
            today = date.today()
            start_date = end_date = None
            period_title = ""
            
            if period == "today":
                start_date = end_date = today
                period_title = "Gastos de Hoje"
            elif period == "week":
                start_date = today - timedelta(days=today.weekday())
                end_date = today
                period_title = "Gastos desta Semana"
            elif period == "month":
                start_date = today.replace(day=1)
                end_date = today
                period_title = "Gastos deste Mês"
            
            # Buscar gastos
            expenses = Expense.get_user_expenses(db, user.id, start_date, end_date)
            
            # IMPORTANTE: Carregar dados relacionados antes de fechar sessão
            expenses_data = []
            for expense in expenses:
                category = expense.category  # Força carregamento
                expenses_data.append({
                    'id': expense.id,
                    'valor': float(expense.valor),
                    'descricao': expense.descricao,
                    'data_gasto': expense.data_gasto,
                    'category_nome': category.nome,
                    'category_icone': category.icone
                })
            
            db.close()
            
            # Formatar mensagem usando dados carregados
            message = ExpenseMessages.expenses_list_message_from_data(expenses_data, period_title)
            keyboard = MainKeyboard.get_back_to_main()
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao buscar gastos: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def handle_text_input(self, update: Update, message_text: str):
        """Manipular entrada de texto do usuário"""
        user_id = update.effective_user.id
        state = state_manager.get_state(user_id)
        
        self._debug_user_state(user_id, f"TEXT INPUT: '{message_text}'")
        
        if state == ConversationState.WAITING_AMOUNT:
            await self._process_amount_input(update, message_text)
        elif state == ConversationState.WAITING_DESCRIPTION:
            await self._process_description_input(update, message_text)
        else:
            logger.warning(f"Texto recebido em estado inesperado: {state}")
    
    async def _process_amount_input(self, update: Update, amount_text: str):
        """Processar entrada de valor"""
        user_id = update.effective_user.id
        
        try:
            logger.info(f"Processando valor '{amount_text}' para usuário {user_id}")
            
            # Limpar e converter valor
            amount_clean = re.sub(r'[^\d,.]', '', amount_text)
            amount_clean = amount_clean.replace(',', '.')
            
            amount = float(amount_clean)
            
            if amount <= 0:
                raise ValueError("Valor deve ser positivo")
            
            # Obter dados atuais do estado
            current_data = state_manager.get_data(user_id)
            category_id = current_data.get('category_id')
            
            logger.info(f"Dados atuais antes de salvar valor: {current_data}")
            
            if not category_id:
                logger.error("Category_id não encontrado no estado!")
                await update.message.reply_text("❌ Erro: categoria perdida. Tente novamente.")
                return
            
            # Atualizar dados do estado COM PRESERVAÇÃO
            state_manager.update_data(user_id, 'amount', amount)
            
            # Verificar se dados foram salvos
            updated_data = state_manager.get_data(user_id)
            logger.info(f"Dados após salvar valor: {updated_data}")
            
            # Buscar categoria para confirmação
            db = SessionLocal()
            category = db.query(Category).filter(Category.id == category_id).first()
            db.close()
            
            if not category:
                await update.message.reply_text("❌ Categoria não encontrada.")
                return
            
            # Mostrar confirmação
            message = ExpenseMessages.confirm_expense_message(
                amount, category.nome, category.icone
            )
            keyboard = ExpenseKeyboard.get_description_options()
            
            # IMPORTANTE: Manter dados ao mudar estado
            state_manager.set_state(
                user_id, 
                ConversationState.CONFIRMING_EXPENSE,
                updated_data  # Passar dados existentes
            )
            
            self._debug_user_state(user_id, "APÓS CONFIRMAR VALOR")
            
            await update.message.reply_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except (ValueError, TypeError) as e:
            logger.error(f"Erro ao processar valor: {e}")
            message = ExpenseMessages.invalid_amount_message()
            await update.message.reply_text(message, parse_mode='Markdown')
    
    async def _process_description_input(self, update: Update, description: str):
        """Processar entrada de descrição"""
        user_id = update.effective_user.id
        
        # Atualizar descrição nos dados PRESERVANDO os existentes
        state_manager.update_data(user_id, 'description', description)
        
        self._debug_user_state(user_id, "APÓS ADICIONAR DESCRIÇÃO")
        
        # Confirmar gasto automaticamente
        await self._save_expense_from_message(update)
    
    async def _request_description(self, query):
        """Solicitar descrição do gasto"""
        user_id = query.from_user.id
        
        self._debug_user_state(user_id, "ANTES DE SOLICITAR DESCRIÇÃO")
        
        message = ExpenseMessages.enter_description_message()
        
        # Manter dados ao mudar estado
        current_data = state_manager.get_data(user_id)
        state_manager.set_state(user_id, ConversationState.WAITING_DESCRIPTION, current_data)
        
        self._debug_user_state(user_id, "APÓS SOLICITAR DESCRIÇÃO")
        
        await query.edit_message_text(message, parse_mode='Markdown')
    
    async def _confirm_expense_callback(self, query):
        """Confirmar e salvar gasto sem descrição (via callback)"""
        user_id = query.from_user.id
        
        self._debug_user_state(user_id, "ANTES DE CONFIRMAR CALLBACK")
        
        await self._save_expense_from_callback(query)
    
    async def _save_expense_from_callback(self, query):
        """Salvar gasto via callback (botão)"""
        user_id = query.from_user.id
        
        try:
            # Obter dados do estado
            data = state_manager.get_data(user_id)
            category_id = data.get('category_id')
            amount = data.get('amount')
            description = data.get('description')
            
            logger.info(f"Salvando gasto via callback - User: {user_id}")
            logger.info(f"    Dados completos: {data}")
            logger.info(f"    Category: {category_id}, Amount: {amount}")
            
            if not category_id or not amount:
                logger.error(f"Dados incompletos - Category: {category_id}, Amount: {amount}")
                
                # Mostrar estado completo para debug
                self._debug_user_state(user_id, "ERRO - DADOS INCOMPLETOS")
                
                await query.edit_message_text(
                    "❌ Dados incompletos. Tente registrar o gasto novamente.",
                    reply_markup=MainKeyboard.get_main_menu()
                )
                return
            
            # Buscar usuário
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                db.close()
                return
            
            # Criar gasto
            logger.info(f"Criando gasto: user_id={user.id}, category_id={category_id}, amount={amount}")
            expense = Expense.create_expense(
                db, user.id, category_id, amount, description
            )
            
            if not expense:
                logger.error("Falha ao criar expense no banco")
                await query.edit_message_text("❌ Erro ao salvar gasto.")
                db.close()
                return
            
            # IMPORTANTE: Carregar categoria antes de fechar sessão
            category = expense.category  # Força o carregamento da categoria
            expense_data = {
                'id': expense.id,
                'valor': float(expense.valor),
                'descricao': expense.descricao,
                'data_gasto': expense.data_gasto,
                'category_nome': category.nome,
                'category_icone': category.icone
            }
            
            db.close()
            
            # Limpar estado
            state_manager.clear_state(user_id)
            
            # Mostrar confirmação usando dados carregados
            message = ExpenseMessages.expense_saved_message_from_data(expense_data)
            keyboard = MainKeyboard.get_main_menu()
            
            await query.edit_message_text(
                message, 
                reply_markup=keyboard, 
                parse_mode='Markdown'
            )
            
            logger.info(f"✅ Gasto salvo com sucesso: ID {expense_data['id']}, Valor: R$ {expense_data['valor']:.2f}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar gasto via callback: {e}")
            await query.edit_message_text("❌ Erro interno ao salvar gasto.")
    
    async def _save_expense_from_message(self, update: Update):
        """Salvar gasto via mensagem de texto"""
        user_id = update.effective_user.id
        
        try:
            # Obter dados do estado
            data = state_manager.get_data(user_id)
            category_id = data.get('category_id')
            amount = data.get('amount')
            description = data.get('description')
            
            if not category_id or not amount:
                await update.message.reply_text("❌ Dados incompletos. Tente novamente.")
                return
            
            # Buscar usuário
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                await update.message.reply_text("❌ Usuário não encontrado.")
                db.close()
                return
            
            # Criar gasto
            expense = Expense.create_expense(
                db, user.id, category_id, amount, description
            )
            
            if not expense:
                await update.message.reply_text("❌ Erro ao salvar gasto.")
                db.close()
                return
            
            # IMPORTANTE: Carregar categoria antes de fechar sessão
            category = expense.category  # Força o carregamento da categoria
            expense_data = {
                'id': expense.id,
                'valor': float(expense.valor),
                'descricao': expense.descricao,
                'data_gasto': expense.data_gasto,
                'category_nome': category.nome,
                'category_icone': category.icone
            }
            
            db.close()
            
            # Limpar estado
            state_manager.clear_state(user_id)
            
            # Mostrar confirmação usando dados carregados
            message = ExpenseMessages.expense_saved_message_from_data(expense_data)
            keyboard = MainKeyboard.get_main_menu()
            
            await update.message.reply_text(
                message, 
                reply_markup=keyboard, 
                parse_mode='Markdown'
            )
            
            logger.info(f"✅ Gasto salvo com sucesso: ID {expense_data['id']}, Valor: R$ {expense_data['valor']:.2f}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar gasto via mensagem: {e}")
            await update.message.reply_text("❌ Erro interno ao salvar gasto.")
    
    async def _cancel_expense(self, query):
        """Cancelar registro de gasto"""
        user_id = query.from_user.id
        state_manager.clear_state(user_id)
        
        message = ExpenseMessages.expense_cancelled_message()
        keyboard = MainKeyboard.get_main_menu()
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    
    async def confirm_pending_action(self, query):
        """Confirmar ação pendente"""
        # Redirecionar para salvar gasto via callback
        await self._save_expense_from_callback(query)