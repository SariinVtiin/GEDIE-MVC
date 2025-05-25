#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test():
    from src.services.gemini_service import gemini_service
    print("🤖 Testando conexão com Gemini...")
    
    # Criar imagem de teste simples
    from PIL import Image
    import io
    
    img = Image.new('RGB', (200, 300), color='white')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    
    result = await gemini_service.analyze_receipt(img_bytes.getvalue())
    print(f"✅ Teste OK: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())