"""
Configuração de logging para GEDIE
"""

import sys
from loguru import logger
from decouple import config

def setup_logging():
    """Configurar sistema de logging"""
    
    # Remover handler padrão
    logger.remove()
    
    # Configurar nível de log
    log_level = config('LOG_LEVEL', default='INFO')
    log_file = config('LOG_FILE', default='logs/gedie.log')
    
    # Handler para console
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        colorize=True
    )
    
    # Handler para arquivo
    logger.add(
        log_file,
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    logger.info("📝 Sistema de logging configurado")