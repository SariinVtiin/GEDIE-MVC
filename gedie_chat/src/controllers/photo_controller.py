"""
Controlador para análise de fotos - VERSÃO SIMPLIFICADA
"""

from telegram import Update, File
from telegram.ext import ContextTypes
from loguru import logger
from typing import Optional, Dict, Any

from services.gemini_service import gemini_service
from config.database_config import SessionLocal
from models.user_model import User
from models.category_model import Category
from models.expense_model import Expense
from views.keyboards.main_keyboard import MainKeyboard
from utils.state_manager import state_manager, ConversationState

class PhotoController:
    """Controlador para análise de comprovantes por foto"""
    
    async def handle_photo_callback(self, query, parts):
        """Manipular callbacks de foto"""
        
        if len(parts) < 2:
            return
        
        subaction = parts[1]
        
        if subaction == "guide":
            await self._show_photo_guide(query)
        elif subaction == "confirm":
            await self._confirm_photo_expense(query)
        elif subaction == "cancel":
            await self._cancel_photo_expense(query)
    
    async def _show_photo_guide(self, query):
        """Mostrar guia de fotos"""
        message = """📷 **Como enviar comprovante**

🎯 **Para melhor análise da IA:**

📸 **Qualidade da foto:**
• Foto clara e bem iluminada
• Evite reflexos e sombras
• Mantenha o celular firme

🧾 **Comprovante visível:**
• Valor total bem legível
• Nome do estabelecimento claro

📱 **Tipos aceitos:**
• Nota fiscal (NFe/NFCe)
• Cupom fiscal
• Recibo de compra
• Comprovante PIX

🤖 **A IA irá identificar:**
• 💰 Valor total pago
• 🏪 Nome do estabelecimento  
• 🏷️ Categoria sugerida

**📸 Envie sua foto agora!**

*Ou use registro manual abaixo:*"""

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = [
            [
                InlineKeyboardButton("💰 Registro Manual", callback_data="expense:register")
            ],
            [
                InlineKeyboardButton("🔙 Menu Principal", callback_data="main:menu")
            ]
        ]
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processar foto enviada"""
        
        user_id = update.effective_user.id
        
        try:
            logger.info(f"📷 Foto recebida do usuário {user_id}")
            
            # Mostrar mensagem de processamento
            processing_message = await update.message.reply_text(
                "📷 **Analisando comprovante...**\n\n"
                "🤖 Usando IA para extrair informações...\n"
                "⏳ Isso pode levar alguns segundos...",
                parse_mode='Markdown'
            )
            
            # Baixar foto
            photo = update.message.photo[-1]  # Maior resolução
            file: File = await photo.get_file()
            
            # Verificar tamanho
            if file.file_size > 20 * 1024 * 1024:  # 20MB
                await processing_message.edit_text(
                    "❌ **Arquivo muito grande**\n\n"
                    "Envie uma foto menor que 20MB.",
                    parse_mode='Markdown'
                )
                return
            
            image_data = await file.download_as_bytearray()
            logger.info(f"Foto baixada: {len(image_data)} bytes")
            
            # Analisar com Gemini
            analysis_result = await gemini_service.analyze_receipt(bytes(image_data))
            
            # Verificar se houve erro
            if analysis_result.get('erro'):
                await processing_message.edit_text(
                    f"❌ **Erro na análise**\n\n"
                    f"{analysis_result.get('observacoes', 'Erro desconhecido')}\n\n"
                    f"💡 Dicas:\n"
                    f"• Foto clara e bem iluminada\n"
                    f"• Valor total visível\n"
                    f"• Tente novamente ou registre manualmente",
                    parse_mode='Markdown'
                )
                return
            
            # Mostrar resultado
            await self._show_analysis_result(processing_message, analysis_result, user_id)
            
        except Exception as e:
            logger.error(f"Erro ao processar foto: {e}")
            await update.message.reply_text(
                "❌ **Erro ao processar foto**\n\n"
                "Tente novamente ou use registro manual.",
                parse_mode='Markdown'
            )
    
    async def _show_analysis_result(self, message, analysis_result: dict, user_id: int):
        """Mostrar resultado da análise"""
        
        try:
            valor = analysis_result.get('valor_total')
            estabelecimento = analysis_result.get('estabelecimento')
            confianca = analysis_result.get('confianca', 0)
            
            # Buscar categoria sugerida
            suggested_category = await self._find_suggested_category(
                user_id, 
                analysis_result.get('categoria_sugerida', 'outros')
            )
            
            # Formatação da confiança
            if confianca >= 0.8:
                confidence_icon = "🟢"
                confidence_text = "Alta"
            elif confianca >= 0.6:
                confidence_icon = "🟡"
                confidence_text = "Boa"
            else:
                confidence_icon = "🔴"
                confidence_text = "Baixa"
            
            # Mensagem de resultado
            result_message = f"🤖 **Análise do Comprovante**\n\n"
            
            if valor and valor > 0:
                valor_formatado = f"R$ {valor:.2f}".replace('.', ',')
                result_message += f"💰 **Valor:** {valor_formatado}\n"
            else:
                result_message += f"💰 **Valor:** ❌ Não identificado\n"
            
            if estabelecimento:
                result_message += f"🏪 **Local:** {estabelecimento}\n"
            
            if suggested_category:
                result_message += f"🏷️ **Categoria:** {suggested_category['icone']} {suggested_category['nome']}\n"
            
            result_message += f"🎯 **Confiança:** {confidence_icon} {confidence_text} ({confianca:.0%})\n\n"
            
            if confianca < 0.6:
                result_message += "⚠️ **Atenção:** Confiança baixa. Verifique os dados.\n\n"
            
            result_message += "**Confirme ou cancele:**"
            
            # Salvar no estado
            state_data = {
                'photo_analysis': analysis_result,
                'source': 'photo'
            }
            
            if suggested_category:
                state_data['category_id'] = suggested_category['id']
            
            state_manager.set_state(user_id, ConversationState.CONFIRMING_EXPENSE, state_data)
            
            # Keyboard de confirmação
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            keyboard = [
                [
                    InlineKeyboardButton("✅ Confirmar Gasto", callback_data="photo:confirm")
                ],
                [
                    InlineKeyboardButton("❌ Cancelar", callback_data="photo:cancel")
                ]
            ]
            
            await message.edit_text(
                result_message,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao mostrar resultado: {e}")
            await message.edit_text("❌ Erro ao processar resultado.")
    
    async def _find_suggested_category(self, user_id: int, suggested_category: str) -> Optional[Dict]:
        """Encontrar categoria sugerida"""
        
        try:
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                db.close()
                return None
            
            # Mapear categoria para nomes em português
            category_mapping = {
                'alimentacao': ['Alimentação', 'Comida', 'Restaurante'],
                'transporte': ['Transporte', 'Combustível', 'Uber'],
                'casa': ['Casa', 'Moradia', 'Lar'],
                'saude': ['Saúde', 'Farmácia', 'Médico'],
                'lazer': ['Lazer', 'Entretenimento', 'Diversão'],
                'outros': ['Outros', 'Diversos']
            }
            
            # Buscar categoria correspondente
            possible_names = category_mapping.get(suggested_category, ['Outros'])
            
            for name in possible_names:
                category = db.query(Category).filter(
                    Category.user_id == user.id,
                    Category.nome.ilike(f'%{name}%'),
                    Category.ativo == True
                ).first()
                
                if category:
                    result = {
                        'id': category.id,
                        'nome': category.nome,
                        'icone': category.icone
                    }
                    db.close()
                    return result
            
            # Se não encontrou, pegar primeira categoria
            first_category = db.query(Category).filter(
                Category.user_id == user.id,
                Category.ativo == True
            ).first()
            
            db.close()
            
            if first_category:
                return {
                    'id': first_category.id,
                    'nome': first_category.nome,
                    'icone': first_category.icone
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar categoria: {e}")
            return None
    
    async def _confirm_photo_expense(self, query):
        """Confirmar gasto da foto"""
        
        user_id = query.from_user.id
        
        try:
            # Obter dados da análise
            data = state_manager.get_data(user_id)
            analysis = data.get('photo_analysis')
            
            if not analysis or not analysis.get('valor_total'):
                await query.edit_message_text("❌ Dados perdidos. Tente novamente.")
                return
            
            # Buscar usuário
            db = SessionLocal()
            user = User.get_by_telegram_id(db, user_id)
            
            if not user:
                await query.edit_message_text("❌ Usuário não encontrado.")
                db.close()
                return
            
            # Usar categoria sugerida ou primeira disponível
            category_id = data.get('category_id')
            if not category_id:
                first_category = db.query(Category).filter(
                    Category.user_id == user.id,
                    Category.ativo == True
                ).first()
                
                if not first_category:
                    await query.edit_message_text("❌ Nenhuma categoria disponível.")
                    db.close()
                    return
                
                category_id = first_category.id
            
            # Criar descrição automática
            estabelecimento = analysis.get('estabelecimento', 'Comprovante')
            descricao = f"📷 {estabelecimento}"
            
            # Criar gasto
            expense = Expense.create_expense(
                db, 
                user.id, 
                category_id, 
                analysis['valor_total'],
                descricao
            )
            
            if not expense:
                await query.edit_message_text("❌ Erro ao salvar gasto.")
                db.close()
                return
            
            # Carregar dados para mensagem
            category = expense.category
            valor_formatado = f"R$ {float(expense.valor):.2f}".replace('.', ',')
            
            db.close()
            
            # Limpar estado
            state_manager.clear_state(user_id)
            
            # Mostrar confirmação
            message = f"""📷 **Gasto registrado por foto!**

💰 **Valor:** {valor_formatado}
{category.icone} **Categoria:** {category.nome}
📅 **Data:** {expense.data_gasto.strftime('%d/%m/%Y')}
📝 **Descrição:** {expense.descricao}

🎉 **Gasto salvo com sucesso!**"""
            
            keyboard = MainKeyboard.get_main_menu()
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
            logger.info(f"✅ Gasto por foto salvo: ID {expense.id}")
            
        except Exception as e:
            logger.error(f"Erro ao confirmar gasto por foto: {e}")
            await query.edit_message_text("❌ Erro interno.")
    
    async def _cancel_photo_expense(self, query):
        """Cancelar gasto por foto"""
        
        user_id = query.from_user.id
        state_manager.clear_state(user_id)
        
        message = "❌ **Análise cancelada**\n\nVocê pode tentar novamente quando quiser."
        
        await query.edit_message_text(
            message,
            reply_markup=MainKeyboard.get_main_menu(),
            parse_mode='Markdown'
        )