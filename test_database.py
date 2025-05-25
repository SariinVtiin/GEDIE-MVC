#!/usr/bin/env python3
"""
Teste de configuração do banco de dados
"""

import sys
import os

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config.logging_config import setup_logging
from config.database_config import test_connection, create_tables, SessionLocal
from models.user_model import User
from models.category_model import Category
from models.expense_model import Expense
from loguru import logger

def test_database():
    """Testar configuração completa do banco"""
    
    setup_logging()
    logger.info("🗄️ Testando configuração do banco de dados...")
    
    # Testar conexão
    if not test_connection():
        logger.error("❌ Falha na conexão com o banco")
        return False
    
    # Criar tabelas
    logger.info("📋 Criando tabelas...")
    if not create_tables():
        logger.error("❌ Falha ao criar tabelas")
        return False
    
    # Testar operações CRUD básicas
    logger.info("🧪 Testando operações CRUD...")
    
    try:
        db = SessionLocal()
        
        # Criar usuário de teste
        logger.info("👤 Criando usuário de teste...")
        user = User.create_user(db, 123456789, "Usuário Teste")
        if not user:
            logger.error("❌ Falha ao criar usuário")
            return False
        
        logger.info(f"✅ Usuário criado: ID {user.id}")
        
        # Criar categorias padrão
        logger.info("🏷️ Criando categorias padrão...")
        categories = Category.create_default_categories(db, user.id)
        if not categories:
            logger.error("❌ Falha ao criar categorias")
            return False
        
        logger.info(f"✅ {len(categories)} categorias criadas")
        
        # Criar gasto de teste
        logger.info("💰 Criando gasto de teste...")
        expense = Expense.create_expense(
            db, 
            user.id, 
            categories[0].id, 
            25.50, 
            "Teste de gasto"
        )
        if not expense:
            logger.error("❌ Falha ao criar gasto")
            return False
        
        logger.info(f"✅ Gasto criado: {expense.format_valor()}")
        
        # Buscar dados
        logger.info("🔍 Testando consultas...")
        found_user = User.get_by_telegram_id(db, 123456789)
        user_categories = Category.get_user_categories(db, user.id)
        user_expenses = Expense.get_today_expenses(db, user.id)
        month_total = Expense.get_month_total(db, user.id)
        
        logger.info(f"✅ Usuário encontrado: {found_user.nome}")
        logger.info(f"✅ Categorias do usuário: {len(user_categories)}")
        logger.info(f"✅ Gastos de hoje: {len(user_expenses)}")
        logger.info(f"✅ Total do mês: R$ {month_total:.2f}")
        
        # Limpar dados de teste
        logger.info("🧹 Limpando dados de teste...")
        expense.delete(db)
        for category in categories:
            category.delete(db)
        user.delete(db)
        
        db.close()
        
        logger.info("🎉 Todos os testes passaram! Banco configurado corretamente!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro durante os testes: {e}")
        return False

if __name__ == "__main__":
    if test_database():
        logger.info("✅ Banco de dados pronto para uso!")
    else:
        logger.error("💥 Problemas na configuração do banco")