"""
Controlador de usuários
"""

from typing import Optional
from loguru import logger
from config.database_config import SessionLocal
from models.user_model import User
from models.category_model import Category

class UserController:
    """Controlador para operações de usuário"""
    
    async def get_or_create_user(self, telegram_id: int, name: str) -> Optional[User]:
        """Buscar usuário existente ou criar novo"""
        try:
            db = SessionLocal()
            
            # Buscar usuário existente
            user = User.get_by_telegram_id(db, telegram_id)
            
            if user:
                logger.info(f"Usuário encontrado: {user.nome} (ID: {user.id})")
                db.close()
                return user
            
            # Criar novo usuário
            logger.info(f"Criando novo usuário: {name} ({telegram_id})")
            user = User.create_user(db, telegram_id, name)
            
            if user:
                # Criar categorias padrão
                categories = Category.create_default_categories(db, user.id)
                logger.info(f"Usuário criado com {len(categories)} categorias padrão")
            
            db.close()
            return user
            
        except Exception as e:
            logger.error(f"Erro ao buscar/criar usuário {telegram_id}: {e}")
            return None
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Buscar usuário pelo Telegram ID"""
        try:
            db = SessionLocal()
            user = User.get_by_telegram_id(db, telegram_id)
            db.close()
            return user
        except Exception as e:
            logger.error(f"Erro ao buscar usuário {telegram_id}: {e}")
            return None
    
    async def update_user_settings(self, telegram_id: int, **kwargs) -> bool:
        """Atualizar configurações do usuário"""
        try:
            db = SessionLocal()
            user = User.get_by_telegram_id(db, telegram_id)
            
            if not user:
                db.close()
                return False
            
            # Atualizar campos permitidos
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            user.save(db)
            db.close()
            
            logger.info(f"Configurações do usuário {telegram_id} atualizadas")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário {telegram_id}: {e}")
            return False