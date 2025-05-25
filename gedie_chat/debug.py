#!/usr/bin/env python3
"""
Script de debug avançado para GEDIE
Monitoramento em tempo real dos estados
"""

import sys
import os
import time

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config.logging_config import setup_logging
from config.database_config import SessionLocal
from models.user_model import User
from models.category_model import Category
from models.expense_model import Expense
from utils.state_manager import state_manager
from loguru import logger

def debug_user_complete(telegram_id):
    """Debug completo de um usuário específico"""
    
    setup_logging()
    logger.info(f"🔍 DEBUG COMPLETO do usuário {telegram_id}")
    
    try:
        # Estado na memória
        print(f"\n📊 ESTADO NA MEMÓRIA:")
        state = state_manager.get_state(telegram_id)
        data = state_manager.get_data(telegram_id)
        print(f"   Estado: {state}")
        print(f"   Dados: {data}")
        
        # Verificar no banco de dados
        print(f"\n🗄️ DADOS NO BANCO:")
        db = SessionLocal()
        
        user = User.get_by_telegram_id(db, telegram_id)
        if user:
            print(f"   👤 Usuário: {user.nome} (ID: {user.id})")
            
            # Categorias
            categories = Category.get_user_categories(db, user.id)
            print(f"   🏷️ Categorias ({len(categories)}):")
            for cat in categories:
                print(f"      • {cat.icone} {cat.nome} (ID: {cat.id})")
            
            # Gastos recentes
            expenses = Expense.get_today_expenses(db, user.id)
            print(f"   💰 Gastos de hoje ({len(expenses)}):")
            for exp in expenses:
                print(f"      • R$ {float(exp.valor):.2f} - {exp.category.nome}")
        else:
            print(f"   ❌ Usuário {telegram_id} não encontrado no banco")
        
        db.close()
        
        # Estados de todos os usuários
        print(f"\n👥 TODOS OS ESTADOS ATIVOS:")
        all_states = state_manager.list_all_states()
        if all_states:
            for user_id, state_info in all_states.items():
                print(f"   • User {user_id}: {state_info}")
        else:
            print("   (Nenhum estado ativo)")
        
    except Exception as e:
        logger.error(f"Erro no debug: {e}")

def monitor_user_real_time(telegram_id, interval=2):
    """Monitorar usuário em tempo real"""
    
    setup_logging()
    logger.info(f"🔄 MONITORAMENTO em tempo real do usuário {telegram_id}")
    print(f"⏰ Atualizando a cada {interval} segundos (Ctrl+C para parar)\n")
    
    try:
        while True:
            # Limpar tela (funciona no Windows e Linux)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"🔄 MONITORAMENTO TEMPO REAL - Usuário {telegram_id}")
            print(f"⏰ {time.strftime('%H:%M:%S')}")
            print("=" * 50)
            
            # Estado atual
            state = state_manager.get_state(telegram_id)
            data = state_manager.get_data(telegram_id)
            
            print(f"📊 Estado: {state}")
            print(f"📋 Dados: {data}")
            
            # Verificar se há dados críticos
            if data:
                category_id = data.get('category_id')
                amount = data.get('amount')
                description = data.get('description')
                
                print(f"\n🔍 ANÁLISE:")
                print(f"   Category ID: {category_id} {'✅' if category_id else '❌'}")
                print(f"   Amount: {amount} {'✅' if amount else '❌'}")
                print(f"   Description: {description if description else '(não definido)'}")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Monitoramento interrompido")

def clear_user_state(telegram_id):
    """Limpar estado de um usuário"""
    state_manager.clear_state(telegram_id)
    print(f"🧹 Estado do usuário {telegram_id} limpo")

def simulate_expense_flow(telegram_id, category_id, amount):
    """Simular fluxo de despesa para teste"""
    
    setup_logging()
    logger.info(f"🧪 SIMULANDO fluxo de despesa")
    
    print(f"1. Limpando estado...")
    state_manager.clear_state(telegram_id)
    
    print(f"2. Definindo SELECTING_CATEGORY...")
    state_manager.set_state(telegram_id, state_manager.ConversationState.SELECTING_CATEGORY)
    
    print(f"3. Salvando category_id = {category_id}...")
    state_manager.set_state(
        telegram_id, 
        state_manager.ConversationState.WAITING_AMOUNT,
        {'category_id': category_id}
    )
    
    print(f"4. Salvando amount = {amount}...")
    state_manager.update_data(telegram_id, 'amount', amount)
    
    print(f"5. Mudando para CONFIRMING_EXPENSE...")
    current_data = state_manager.get_data(telegram_id)
    state_manager.set_state(
        telegram_id,
        state_manager.ConversationState.CONFIRMING_EXPENSE,
        current_data
    )
    
    print(f"\n✅ RESULTADO FINAL:")
    final_state = state_manager.get_state(telegram_id)
    final_data = state_manager.get_data(telegram_id)
    print(f"   Estado: {final_state}")
    print(f"   Dados: {final_data}")

def list_all_states():
    """Listar todos os estados ativos"""
    setup_logging()
    
    print("📋 TODOS OS ESTADOS ATIVOS:")
    all_states = state_manager.list_all_states()
    
    if all_states:
        for user_id, state_info in all_states.items():
            print(f"   • User {user_id}: {state_info}")
    else:
        print("   (Nenhum estado ativo)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("📖 USO DO SCRIPT DE DEBUG:")
        print("")
        print("  python debug.py debug <telegram_id>")
        print("    • Debug completo de um usuário")
        print("")
        print("  python debug.py monitor <telegram_id> [intervalo]")
        print("    • Monitorar usuário em tempo real")
        print("")
        print("  python debug.py clear <telegram_id>") 
        print("    • Limpar estado de um usuário")
        print("")
        print("  python debug.py simulate <telegram_id> <category_id> <amount>")
        print("    • Simular fluxo completo de despesa")
        print("")
        print("  python debug.py list")
        print("    • Listar todos os estados ativos")
        print("")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "debug" and len(sys.argv) > 2:
        telegram_id = int(sys.argv[2])
        debug_user_complete(telegram_id)
        
    elif command == "monitor" and len(sys.argv) > 2:
        telegram_id = int(sys.argv[2])
        interval = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        monitor_user_real_time(telegram_id, interval)
        
    elif command == "clear" and len(sys.argv) > 2:
        telegram_id = int(sys.argv[2])
        clear_user_state(telegram_id)
        
    elif command == "simulate" and len(sys.argv) > 4:
        telegram_id = int(sys.argv[2])
        category_id = int(sys.argv[3])
        amount = float(sys.argv[4])
        simulate_expense_flow(telegram_id, category_id, amount)
        
    elif command == "list":
        list_all_states()
        
    else:
        print("❌ Comando inválido ou parâmetros insuficientes!")