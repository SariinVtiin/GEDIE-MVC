"""
TelegramLibrary — Biblioteca Robot Framework baseada no Telethon
----------------------------------------------------------------
Keywords expostas ao Robot:
    Open Connection
    Close Connection / Close All Connections
    Send Command
    Click Button
    Wait For Reply Containing
    Send Image               (novo p/ comprovante)
"""

import os
import asyncio
import time
import re
import unicodedata
import tempfile
import random
import datetime
from typing import Optional

from dotenv import load_dotenv
load_dotenv()  # lê .env

# ---------- Bibliotecas de terceiros ----------
from telethon import TelegramClient, Button
from telethon.errors import SessionPasswordNeededError
from robot.api import logger as rf_logger
from robot.libraries.BuiltIn import BuiltIn
from PIL import Image, ImageDraw

DEFAULT_TIMEOUT = 10  # s

# ---------------- Normalização texto ----------------
_EMOJI_RE = re.compile(
    "["                       # qualquer
    "\U0001F600-\U0001F64F"   # emoticons
    "\U0001F300-\U0001F5FF"   # símbolos & pictogramas
    "\U0001F680-\U0001F6FF"   # transporte & mapas
    "\U0001F1E0-\U0001F1FF"   # bandeiras
    "]+",
    flags=re.UNICODE,
)


def _normalize(text: str) -> str:
    """Lower + sem emojis + sem acentos + sem espaçamentos extras."""
    if not text:
        return ""
    text = _EMOJI_RE.sub("", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.split()).lower()


# ------------- Helper para gerar cupom fiscal fake -------------
def generate_fake_receipt(total="25,00", path: str | None = None) -> str:
    """Gera PNG simples de cupom fiscal e devolve o caminho do arquivo."""
    if path is None:
        fd, path = tempfile.mkstemp(suffix=".png", prefix="receipt_")
        os.close(fd)

    # fundo branco 600x400
    img = Image.new("RGB", (600, 400), "white")
    draw = ImageDraw.Draw(img)
    txt = (
        "CUPOM FISCAL\n\n"
        f"TOTAL: R$ {total}\n"
        f"DATA: {datetime.date.today():%d/%m/%Y}\n"
        f"ID: {random.randint(100000, 999999)}"
    )
    draw.multiline_text((30, 40), txt, fill="black", spacing=4)
    img.save(path)
    return path


# ------------- Classe principal ------------------------------------------------
class TelegramLibrary:
    """Wrapper Telethon exposto ao Robot Framework."""

    def __init__(self):
        self._client: Optional[TelegramClient] = None
        self._loop = asyncio.get_event_loop()
        self._bot_username = os.getenv("TG_BOT_USERNAME", "").lstrip("@")
        if not self._bot_username:
            raise RuntimeError("TG_BOT_USERNAME precisa estar no .env")

    # ---------- Sessão ----------
    def open_connection(self):
        """Login com conta de teste."""
        if self._client and self._client.is_connected():
            return

        api_id = int(os.getenv("TG_API_ID", "0"))
        api_hash = os.getenv("TG_API_HASH")
        phone = os.getenv("TG_PHONE")
        if not all([api_id, api_hash, phone]):
            raise RuntimeError("TG_API_ID / TG_API_HASH / TG_PHONE não definidos")

        self._client = TelegramClient("robotframework-session", api_id, api_hash)
        self._loop.run_until_complete(self._client.connect())

        if not self._loop.run_until_complete(self._client.is_user_authorized()):
            self._loop.run_until_complete(self._client.send_code_request(phone))
            code = BuiltIn().get_variable_value("${TELEGRAM_CODE}", default=None)
            if not code:
                raise RuntimeError("Defina ${TELEGRAM_CODE} com o código SMS")
            try:
                self._loop.run_until_complete(self._client.sign_in(phone, code))
            except SessionPasswordNeededError:
                pw = BuiltIn().get_variable_value("${TELEGRAM_PASSWORD}", default=None)
                if not pw:
                    raise RuntimeError("Conta tem 2FA; defina ${TELEGRAM_PASSWORD}")
                self._loop.run_until_complete(self._client.sign_in(password=pw))

        rf_logger.info("📡 Conexão Telegram OK")

    def close_connection(self):
        """Desconecta, ignorando se já estiver offline."""
        if not self._client:
            return
        disc = self._client.disconnect()
        if asyncio.iscoroutine(disc):
            self._loop.run_until_complete(disc)
        self._client = None
        rf_logger.info("🔌 Conexão Telegram encerrada")

    # alias p/ Suite Teardown
    def close_all_connections(self):
        self.close_connection()

    # ---------- Interações ----------
    def send_command(self, command: str):
        self._ensure_client()
        rf_logger.info(f"➡️ Texto: {command}")
        self._loop.run_until_complete(
            self._client.send_message(self._bot_username, str(command))
        )

    def send_image(self, image_path: str):
        """Keyword para enviar foto/arquivo (comprovante)."""
        self._ensure_client()
        rf_logger.info(f"📤 Imagem: {image_path}")
        self._loop.run_until_complete(
            self._client.send_file(self._bot_username, image_path)
        )

    def click_button(self, button_text: str, timeout: int = DEFAULT_TIMEOUT):
        self._ensure_client()
        expected_n = _normalize(button_text)
        entity = self._loop.run_until_complete(self._client.get_entity(self._bot_username))

        end_time = time.time() + timeout
        while time.time() < end_time:
            history = self._loop.run_until_complete(self._client.get_messages(entity, limit=1))
            if history and history[0].buttons:
                for row in history[0].buttons:
                    for button in row:
                        if expected_n in _normalize(button.text or ""):
                            self._loop.run_until_complete(button.click())
                            rf_logger.info(f"🖱️ Clicado: {button.text}")
                            return
            time.sleep(1)
        raise AssertionError(f"Botão '{button_text}' não encontrado em {timeout}s")

    def wait_for_reply_containing(self, expected: str, timeout: int = DEFAULT_TIMEOUT):
        self._ensure_client()
        expected_n = _normalize(expected)
        entity = self._loop.run_until_complete(self._client.get_entity(self._bot_username))

        end_time = time.time() + timeout
        last_text = ""
        while time.time() < end_time:
            msg = self._loop.run_until_complete(
                self._client.get_messages(entity, limit=1)
            )[0]
            current_text = _normalize(msg.message)
            if current_text != last_text and expected_n in current_text:
                rf_logger.info(f"✅ Encontrado: {msg.message!r}")
                return
            last_text = current_text
            time.sleep(1)
        raise AssertionError(f'Resposta contendo "{expected}" não recebida em {timeout}s')

    # ---------- Interno ----------
    def _ensure_client(self):
        if not self._client or not self._client.is_connected():
            raise RuntimeError("Use `Open Connection` antes.")
