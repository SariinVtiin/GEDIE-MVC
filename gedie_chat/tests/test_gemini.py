# tests/test_gemini.py
"""
Testes que exercitam o Gemini real. Necessitam de GEMINI_API_KEY válida
no ambiente ou em um .env carregado pela aplicação.
"""

import io, pytest
from PIL import Image, ImageDraw
from services.gemini_service import gemini_service

pytestmark = pytest.mark.asyncio

def _dummy_receipt_bytes() -> bytes:
    """Gera um PNG simples representando um cupom (texto impresso)."""
    img = Image.new("RGB", (400, 600), "white")
    drw = ImageDraw.Draw(img)
    drw.rectangle([20, 20, 380, 580], outline="black", width=2)
    drw.text((50, 50), "SUPERMERCADO TESTE LTDA", fill="black")
    drw.text((50, 100), "ARROZ 5KG               25,90", fill="black")
    drw.text((50, 130), "FEIJAO 1KG              8,50", fill="black")
    drw.text((50, 180), "TOTAL A PAGAR      R$ 34,40", fill="black")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def _skip_if_no_key():
    if not gemini_service.api_key or gemini_service.api_key.startswith("fake"):
        pytest.skip("GEMINI_API_KEY não configurada")

# --------------------------------------------------------------------------- #
# Testes
# --------------------------------------------------------------------------- #
async def test_gemini_connection():
    _skip_if_no_key()
    assert gemini_service.test_connection() is True

async def test_gemini_analyze_receipt():
    _skip_if_no_key()

    result = await gemini_service.analyze_receipt(_dummy_receipt_bytes())

    # Estrutura mínima esperada
    assert isinstance(result, dict)
    assert result["valor_total"] and result["valor_total"] > 0
    assert 0.0 <= result["confianca"] <= 1.0
    assert result["categoria_sugerida"] in {
        "alimentacao", "transporte", "casa", "saude", "lazer", "outros"
    }
