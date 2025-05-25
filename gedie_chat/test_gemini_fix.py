#!/usr/bin/env python3
"""
Teste da correção do Gemini Service
"""

import sys
import os
import asyncio

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.gemini_service import gemini_service
from loguru import logger
from src.config.logging_config import setup_logging

async def test_gemini_fix():
    """Testar se o Gemini está funcionando com o novo modelo"""
    
    setup_logging()
    
    print("🔧 GEDIE - Teste da Correção do Gemini")
    print("=" * 40)
    
    # Teste 1: Conexão básica
    print("1. 🔗 Testando conexão com novo modelo...")
    
    try:
        if gemini_service.test_connection():
            print("   ✅ Conexão OK com gemini-1.5-flash!")
        else:
            print("   ❌ Falha na conexão")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Análise de imagem simples
    print("\n2. 🖼️ Testando análise de imagem...")
    
    try:
        # Criar imagem de teste simples
        from PIL import Image, ImageDraw
        import io
        
        # Criar comprovante fictício
        image = Image.new('RGB', (400, 600), color='white')
        draw = ImageDraw.Draw(image)
        
        # Simular comprovante
        draw.rectangle([20, 20, 380, 580], outline='black', width=2)
        draw.text((50, 50), "SUPERMERCADO TESTE LTDA", fill='black')
        draw.text((50, 100), "ARROZ 5KG               25,90", fill='black')
        draw.text((50, 130), "FEIJAO 1KG              8,50", fill='black')
        draw.text((50, 180), "TOTAL A PAGAR      R$ 34,40", fill='black')
        
        # Converter para bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        print("   📸 Imagem de teste criada")
        print("   🤖 Enviando para análise...")
        
        # Analisar com Gemini
        result = await gemini_service.analyze_receipt(img_bytes)
        
        print(f"\n   📊 RESULTADO DA ANÁLISE:")
        print(f"   💰 Valor: {result.get('valor_total', 'N/A')}")
        print(f"   🏪 Estabelecimento: {result.get('estabelecimento', 'N/A')}")
        print(f"   🏷️ Categoria: {result.get('categoria_sugerida', 'N/A')}")
        print(f"   🎯 Confiança: {result.get('confianca', 0):.0%}")
        
        if result.get('erro'):
            print(f"   ⚠️ Erro: {result.get('observacoes', '')}")
            return False
        else:
            print("   ✅ Análise realizada com sucesso!")
            return True
            
    except Exception as e:
        print(f"   ❌ Erro no teste de análise: {e}")
        return False

async def main():
    """Função principal"""
    
    success = await test_gemini_fix()
    
    print(f"\n🎯 RESULTADO FINAL:")
    print("=" * 20)
    
    if success:
        print("🎉 CORREÇÃO APLICADA COM SUCESSO!")
        print("✅ Gemini 1.5 Flash funcionando")
        print("✅ Análise de imagem OK")
        print(f"\n🚀 Agora teste no bot:")
        print("   1. python main.py")
        print("   2. Envie foto no Telegram")
    else:
        print("❌ AINDA HÁ PROBLEMAS")
        print("Verifique a API key e conexão")

if __name__ == "__main__":
    asyncio.run(main())