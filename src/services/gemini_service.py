"""
Serviço de integração com Google Gemini - VERSÃO ATUALIZADA
"""

import google.generativeai as genai
import json
from typing import Dict, Any
from PIL import Image
from io import BytesIO
from decouple import config
from loguru import logger

class GeminiService:
    """Serviço para análise de comprovantes com Gemini"""
    
    def __init__(self):
        self.api_key = config('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        
        # CORREÇÃO: Usar modelo atualizado
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        logger.info("🤖 Gemini Service inicializado com modelo gemini-1.5-flash")
    
    async def analyze_receipt(self, image_data: bytes) -> Dict[str, Any]:
        """Analisar comprovante e extrair informações"""
        
        try:
            logger.info(f"Iniciando análise de comprovante ({len(image_data)} bytes)")
            
            # Converter bytes para PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Redimensionar se muito grande
            max_size = 1024
            if image.width > max_size or image.height > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                logger.info(f"Imagem redimensionada para {image.size}")
            
            # Prompt otimizado para comprovantes brasileiros
            prompt = """
Analise esta imagem de comprovante fiscal brasileiro (nota fiscal, cupom, recibo) e extraia as informações em formato JSON.

IMPORTANTE: Responda APENAS o JSON válido, sem texto adicional ou formatação markdown.

{
    "valor_total": 25.50,
    "estabelecimento": "Nome da Loja/Restaurante",
    "categoria_sugerida": "alimentacao",
    "itens_principais": ["item1", "item2", "item3"],
    "confianca": 0.85,
    "observacoes": "Informações relevantes"
}

REGRAS IMPORTANTES:
- valor_total: número decimal do valor TOTAL PAGO (exemplo: 25.50)
- estabelecimento: nome completo da loja/restaurante/empresa
- categoria_sugerida: escolha uma: "alimentacao", "transporte", "casa", "saude", "lazer", "outros"
- itens_principais: até 3 itens mais importantes comprados
- confianca: sua certeza na análise (0.0 a 1.0)
- observacoes: informações adicionais úteis

CATEGORIZAÇÃO:
- "alimentacao": restaurantes, mercados, lanches, delivery, supermercados
- "transporte": combustível, estacionamento, Uber, táxi, ônibus
- "casa": construção, móveis, utensílios, limpeza
- "saude": farmácia, consultas, exames, medicamentos
- "lazer": cinema, eventos, jogos, viagens, entretenimento
- "outros": quando não se encaixar nas demais

Se não conseguir identificar algum campo claramente, use null.
RESPONDA APENAS O JSON, SEM TEXTO ADICIONAL.
"""
            
            # Enviar para Gemini com novo modelo
            logger.info("Enviando para análise do Gemini 1.5 Flash...")
            response = self.model.generate_content([prompt, image])
            
            # Parse da resposta
            response_text = response.text.strip()
            logger.info(f"Resposta bruta do Gemini: {response_text[:200]}...")
            
            # Limpar possível formatação markdown
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            # Tentar encontrar JSON na resposta
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Tentar extrair JSON de uma resposta mais complexa
                import re
                json_match = re.search(r'\{.*?\}', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group()
                    result = json.loads(json_text)
                else:
                    raise ValueError("Não foi possível encontrar JSON válido na resposta")
            
            # Validar e normalizar resultado
            result = self._validate_result(result)
            
            logger.info(f"✅ Análise concluída: valor={result.get('valor_total')}, estabelecimento={result.get('estabelecimento')}, confiança={result.get('confianca')}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao fazer parse do JSON: {e}")
            logger.error(f"Resposta recebida: {response_text}")
            return self._create_error_result("IA retornou formato inválido")
            
        except Exception as e:
            logger.error(f"Erro na análise: {e}")
            return self._create_error_result(f"Erro na análise: {str(e)}")
    
    def _validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validar e normalizar resultado do Gemini"""
        
        # Validar valor_total
        if result.get('valor_total'):
            try:
                # Converter para float
                valor_str = str(result['valor_total']).replace(',', '.')
                valor = float(valor_str)
                if valor > 0:
                    result['valor_total'] = valor
                else:
                    result['valor_total'] = None
            except (ValueError, TypeError):
                logger.warning(f"Valor inválido: {result.get('valor_total')}")
                result['valor_total'] = None
        else:
            result['valor_total'] = None
        
        # Validar estabelecimento
        if not result.get('estabelecimento') or result['estabelecimento'] == 'null':
            result['estabelecimento'] = None
        
        # Validar categoria
        categorias_validas = ['alimentacao', 'transporte', 'casa', 'saude', 'lazer', 'outros']
        if result.get('categoria_sugerida') not in categorias_validas:
            logger.warning(f"Categoria inválida: {result.get('categoria_sugerida')}")
            result['categoria_sugerida'] = 'outros'
        
        # Garantir confiança entre 0 e 1
        try:
            confianca = float(result.get('confianca', 0.5))
            if confianca < 0:
                confianca = 0.0
            elif confianca > 1:
                confianca = 1.0
            result['confianca'] = confianca
        except (ValueError, TypeError):
            result['confianca'] = 0.5
        
        # Limitar itens principais
        if isinstance(result.get('itens_principais'), list):
            # Filtrar itens válidos
            itens_validos = [
                item for item in result['itens_principais'][:3] 
                if item and item != 'null' and isinstance(item, str)
            ]
            result['itens_principais'] = itens_validos
        else:
            result['itens_principais'] = []
        
        # Validar observações
        if not result.get('observacoes') or result['observacoes'] == 'null':
            result['observacoes'] = None
        
        return result
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Criar resultado de erro padronizado"""
        return {
            'valor_total': None,
            'estabelecimento': None,
            'categoria_sugerida': 'outros',
            'itens_principais': [],
            'confianca': 0.0,
            'observacoes': f"Erro: {error_message}",
            'erro': True
        }
    
    def test_connection(self) -> bool:
        """Testar conexão com Gemini API"""
        try:
            logger.info("🧪 Testando conexão com Gemini API...")
            
            # Teste simples com modelo de texto
            model_text = genai.GenerativeModel('gemini-1.5-flash')
            response = model_text.generate_content("Responda apenas: TESTE_OK")
            
            if "TESTE_OK" in response.text:
                logger.info("✅ Conexão com Gemini API funcionando")
                return True
            else:
                logger.warning(f"⚠️ Resposta inesperada: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao testar Gemini API: {e}")
            return False

# Instância global
gemini_service = GeminiService()