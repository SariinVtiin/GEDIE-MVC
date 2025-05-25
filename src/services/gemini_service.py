"""
Serviço de integração com Google Gemini
"""

import google.generativeai as genai
import json
from typing import Dict, Any, Optional
from PIL import Image
from io import BytesIO
from decouple import config
from loguru import logger

class GeminiService:
    """Serviço para análise de comprovantes com Gemini"""
    
    def __init__(self):
        self.api_key = config('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision')
    
    async def analyze_receipt(self, image_data: bytes) -> Dict[str, Any]:
        """Analisar comprovante e extrair informações"""
        
        try:
            # Converter bytes para PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Prompt otimizado para extração de dados
            prompt = """
Analise esta imagem de comprovante/nota fiscal e extraia as seguintes informações em formato JSON:

{
    "valor_total": "XX.XX",
    "estabelecimento": "Nome do estabelecimento",
    "data": "DD/MM/AAAA",
    "categoria_sugerida": "alimentacao|transporte|casa|saude|lazer|outros",
    "itens_principais": ["item1", "item2", "item3"],
    "confianca": 0.95,
    "observacoes": "Informações adicionais relevantes"
}

Regras:
- valor_total deve ser o valor final pago (número com 2 decimais)
- estabelecimento deve ser o nome da loja/restaurante
- data no formato DD/MM/AAAA
- categoria_sugerida baseada no tipo de estabelecimento
- itens_principais: até 3 itens mais relevantes
- confianca: valor de 0 a 1 indicando certeza da análise
- Se não conseguir identificar algo, coloque null

RESPONDA APENAS O JSON, SEM TEXTO ADICIONAL.
"""
            
            # Enviar para Gemini
            response = self.model.generate_content([prompt, image])
            
            # Parse da resposta
            response_text = response.text.strip()
            
            # Limpar possível formatação markdown
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '')
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Validar resultado
            result = self._validate_result(result)
            
            logger.info(f"Análise Gemini concluída: {result}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao fazer parse do JSON do Gemini: {e}")
            logger.error(f"Resposta recebida: {response_text}")
            return self._create_error_result("Erro ao interpretar resposta da IA")
            
        except Exception as e:
            logger.error(f"Erro na análise do Gemini: {e}")
            return self._create_error_result(f"Erro na análise: {str(e)}")
    
    def _validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validar e normalizar resultado do Gemini"""
        
        # Validar valor_total
        if result.get('valor_total'):
            try:
                # Converter para float para validar
                valor = float(str(result['valor_total']).replace(',', '.'))
                result['valor_total'] = valor
            except (ValueError, TypeError):
                result['valor_total'] = None
        
        # Validar categoria
        categorias_validas = ['alimentacao', 'transporte', 'casa', 'saude', 'lazer', 'outros']
        if result.get('categoria_sugerida') not in categorias_validas:
            result['categoria_sugerida'] = 'outros'
        
        # Garantir confiança entre 0 e 1
        if not isinstance(result.get('confianca'), (int, float)) or result['confianca'] < 0 or result['confianca'] > 1:
            result['confianca'] = 0.5
        
        # Limitar itens principais
        if isinstance(result.get('itens_principais'), list):
            result['itens_principais'] = result['itens_principais'][:3]
        else:
            result['itens_principais'] = []
        
        return result
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Criar resultado de erro padronizado"""
        return {
            'valor_total': None,
            'estabelecimento': None,
            'data': None,
            'categoria_sugerida': 'outros',
            'itens_principais': [],
            'confianca': 0.0,
            'observacoes': f"Erro: {error_message}",
            'erro': True
        }

# Instância global
gemini_service = GeminiService()