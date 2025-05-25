#!/usr/bin/env python3
"""
GEDIE - Sistema de Gestão de Gastos
Bot do Telegram com interface por botões
VERSÃO COM DEBUG ATIVADO
"""

import sys
import os

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# IMPORTANTE: Adicionar src ao path ANTES dos imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from telegram.ext import Application
from decouple import config
from loguru import logger

from src.config.logging_config import setup_logging
from src.config.database_config import test_connection, create_tables
from src.controllers.bot_controller import BotController

def main():
    """Função principal da aplicação"""
    
    # Configurar logging com DEBUG
    setup_logging()
    
    # Ativar debug do SQLAlchemy se DEBUG=True
    debug_mode = config('DEBUG', default=False, cast=bool)
    if debug_mode:
        logger.info("🐛 MODO DEBUG ATIVADO")
        # Configurar logging do SQLAlchemy
        import logging
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    logger.info("🚀 Iniciando GEDIE Bot...")
    
    # Verificar configurações
    bot_token = config('TELEGRAM_BOT_TOKEN', default=None)
    if not bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN não configurado!")
        return
    
    # Testar conexão com banco
    logger.info("🗄️ Testando conexão com banco de dados...")
    if not test_connection():
        logger.error("❌ Falha na conexão com o banco!")
        return
    
    # Criar tabelas se necessário
    create_tables()
    
    # Mostrar informações de debug
    if debug_mode:
        mysql_host = config('MYSQL_HOST', default='localhost')
        mysql_db = config('MYSQL_DATABASE', default='gedie_db')
        logger.info(f"🗄️ Conectado ao MySQL: {mysql_host}/{mysql_db}")
        logger.info(f"🤖 Token do Bot: {bot_token[:10]}...{bot_token[-10:]}")
    
    try:
        # Criar aplicação do bot
        application = Application.builder().token(bot_token).build()
        
        # Configurar controladores
        bot_controller = BotController()
        
        # Registrar handlers
        handlers = bot_controller.get_handlers()
        logger.info(f"📋 Registrando {len(handlers)} handlers...")
        
        for handler in handlers:
            application.add_handler(handler)
            logger.debug(f"   ✅ Handler registrado: {type(handler).__name__}")
        
        # Registrar error handler
        application.add_error_handler(bot_controller.error_handler)
        
        logger.info("✅ Todos os handlers registrados com sucesso!")
        
        # Informações de início
        logger.info("🤖 GEDIE Bot está rodando...")
        logger.info("💡 Pressione Ctrl+C para parar")
        
        if debug_mode:
            logger.info("🔍 Debug ativado - logs detalhados disponíveis")
            logger.info("🛠️ Para debug de usuário específico, use:")
            logger.info("     python debug.py monitor <telegram_id>")
        
        # Iniciar bot
        application.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
        
        # Mostrar estados ativos ao parar (se debug ativado)
        if debug_mode:
            from src.utils.state_manager import state_manager
            active_states = state_manager.list_all_states()
            if active_states:
                logger.info("📊 Estados ativos ao parar:")
                for user_id, state_info in active_states.items():
                    logger.info(f"   • User {user_id}: {state_info}")
            else:
                logger.info("📊 Nenhum estado ativo")
                
    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
        if debug_mode:
            import traceback
            logger.error(f"Stack trace: {traceback.format_exc()}")
    finally:
        logger.info("👋 GEDIE Bot finalizado")

if __name__ == "__main__":
    main()