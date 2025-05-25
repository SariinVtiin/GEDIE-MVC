"""
Mensagens para funcionalidade de fotos
"""

from typing import Dict, Any, Optional
from datetime import date

class PhotoMessages:
    """Formatador de mensagens para análise de fotos"""
    
    @staticmethod
    def analysis_result_message(analysis: Dict[str, Any], suggested_category: Optional[Dict]) -> str:
        """Mensagem com resultado da análise"""
        
        valor = analysis.get('valor_total')
        estabelecimento = analysis.get('estabelecimento')
        confianca = analysis.get('confianca', 0)
        itens = analysis.get('itens_principais', [])
        
        # Ícone de confiança
        if confianca >= 0.8:
            confidence_icon = "🟢"
            confidence_text = "Alta"
        elif confianca >= 0.5:
            confidence_icon = "🟡"
            confidence_text = "Média"
        else:
            confidence_icon = "🔴"
            confidence_text = "Baixa"
        
        message = f"🤖 **Análise do Comprovante**\n\n"
        
        if valor:
            message += f"💰 **Valor:** R$ {valor:.2f}\n"
        else:
            message += f"💰 **Valor:** ❌ Não identificado\n"
        
        if estabelecimento:
            message += f"🏪 **Local:** {estabelecimento}\n"
        
        if suggested_category:
            message += f"🏷️ **Categoria:** {suggested_category['icone']} {suggested_category['nome']}\n"
        
        if itens:
            message += f"📝 **Itens:** {', '.join(itens[:3])}\n"
        
        message += f"📊 **Confiança:** {confidence_icon} {confidence_text} ({confianca:.0%})\n"
        message += f"📅 **Data:** {date.today().strftime('%d/%m/%Y')}\n\n"
        
        if confianca < 0.5:
            message += "⚠️ **Atenção:** Confiança baixa. Verifique os dados antes de confirmar.\n\n"
        
        message += "**Confirme ou edite as informações:**"
        
        return message
    
    @staticmethod
    def expense_saved_from_photo_message(expense_data: Dict[str, Any]) -> str:
        """Mensagem de gasto salvo por foto"""
        
        valor_formatado = f"R$ {expense_data['valor']:.2f}".replace('.', ',')
        data_formatada = expense_data['data_gasto'].strftime('%d/%m/%Y')
        confianca = expense_data.get('confianca', 0)
        
        message = f"📷 **Gasto registrado por foto!**\n\n"
        message += f"💰 **Valor:** {valor_formatado}\n"
        message += f"{expense_data['category_icone']} **Categoria:** {expense_data['category_nome']}\n"
        message += f"📅 **Data:** {data_formatada}\n"
        
        if expense_data.get('descricao'):
            message += f"📝 **Descrição:** {expense_data['descricao']}\n"
        
        message += f"🤖 **IA Confiança:** {confianca:.0%}\n\n"
        message += "✅ **Gasto salvo com sucesso!**\n"
        message += "🎯 Use o dashboard web para relatórios detalhados."
        
        return message
    
    @staticmethod
    def edit_value_message(current_value: float) -> str:
        """Mensagem para editar valor"""
        
        valor_atual = f"R$ {current_value:.2f}" if current_value else "Não detectado"
        
        return f"""💰 **Editar Valor**

📊 **Valor atual:** {valor_atual}

Digite o valor correto:
*Exemplo: 25.50 ou 25,50*"""
    
    @staticmethod
    def photo_guide_message() -> str:
        """Guia para envio de fotos"""
        
        return """📷 **Como enviar comprovante**

🎯 **Para melhor análise:**
- Foto clara e bem iluminada
- Valor total visível
- Nome do estabelecimento legível
- Evite reflexos e sombras

📱 **Tipos aceitos:**
- Nota fiscal
- Cupom fiscal
- Recibo de cartão
- Comprovante PIX

🤖 **A IA irá extrair:**
- Valor total
- Nome do estabelecimento  
- Sugestão de categoria
- Itens principais

**📸 Envie a foto agora ou use registro manual:**"""