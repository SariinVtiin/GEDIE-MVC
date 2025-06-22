"""
TelegramLibrary — Biblioteca Robot Framework baseada em Telethon
----------------------------------------------------------------
Keywords disponíveis (para usar nos seus .robot):
    Open Connection
    Close Connection
    Close All Connections   (alias para suite teardown)
    Send Command            (envia texto)
    Click Button            (clica em botão inline)
    Wait For Reply Containing
"""

import os
import asyncio
import time
import re
import unicodedata
from typing import Optional

from dotenv import load_dotenv
load_dotenv()  # lê .env na raiz do projeto

from telethon import TelegramClient, Button
from telethon.errors import SessionPasswordNeededError
from robot.api import logger as rf_logger
from robot.libraries.BuiltIn import BuiltIn

DEFAULT_TIMEOUT = 10  # segundos -----------------------------------------------------------------

# ---------------- Normalização (remove emojis, acentos, espaços múltiplos) ------------------------
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
    """lowercase, sem emojis/acentos e sem múltiplos espaços."""
    if not text:
        return ""
    text = _EMOJI_RE.sub("", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.split()).lower()


# ---------------- Biblioteca principal ------------------------------------------------------------
class TelegramLibrary:
    """Wrapper Telethon exposto ao Robot Framework."""

    def __init__(self):
        self._client: Optional[TelegramClient] = None
        self._loop = asyncio.get_event_loop()

        self._bot_username: str = os.getenv("TG_BOT_USERNAME", "").lstrip("@")
        if not self._bot_username:
            raise RuntimeError("Env var TG_BOT_USERNAME ausente")

    # ---------- Sessão ----------
    def open_connection(self):
        """Abre sessão com a conta de teste (TG_API_ID / TG_API_HASH / TG_PHONE)."""
        if self._client and self._client.is_connected():
            return

        api_id = int(os.getenv("TG_API_ID", "0"))
        api_hash = os.getenv("TG_API_HASH")
        phone = os.getenv("TG_PHONE")
        if not all([api_id, api_hash, phone]):
            raise RuntimeError("TG_API_ID, TG_API_HASH e TG_PHONE devem estar definidos")

        self._client = TelegramClient("robotframework-session", api_id, api_hash)
        self._loop.run_until_complete(self._client.connect())

        if not self._loop.run_until_complete(self._client.is_user_authorized()):
            self._loop.run_until_complete(self._client.send_code_request(phone))
            code = BuiltIn().get_variable_value("${TELEGRAM_CODE}", default=None)
            if not code:
                raise RuntimeError("Informe o código SMS em ${TELEGRAM_CODE}")
            try:
                self._loop.run_until_complete(self._client.sign_in(phone, code))
            except SessionPasswordNeededError:
                pw = BuiltIn().get_variable_value("${TELEGRAM_PASSWORD}", default=None)
                if not pw:
                    raise RuntimeError("Conta tem 2FA; defina ${TELEGRAM_PASSWORD}")
                self._loop.run_until_complete(self._client.sign_in(password=pw))

        rf_logger.info("📡 Conexão Telegram estabelecida")

    def close_connection(self):
        """Fecha a sessão se estiver conectada."""
        if not self._client:
            return
        disc = self._client.disconnect()
        if asyncio.iscoroutine(disc):
            self._loop.run_until_complete(disc)
        self._client = None
        rf_logger.info("🔌 Conexão Telegram encerrada")

    # alias para Suite Teardown
    def close_all_connections(self):
        self.close_connection()

    # ---------- Interações ----------
    def send_command(self, command: str):
        """Envia texto simples para o bot."""
        self._ensure_client()
        rf_logger.info(f"➡️ Enviando: {command}")
        self._loop.run_until_complete(
            self._client.send_message(self._bot_username, str(command))
        )

    def click_button(self, button_text: str, timeout: int = DEFAULT_TIMEOUT):
        """Clica em botão inline que contenha *button_text* (case-insensitive, sem emoji)."""
        self._ensure_client()
        expected_n = _normalize(button_text)
        entity = self._loop.run_until_complete(self._client.get_entity(self._bot_username))

        end_time = time.time() + timeout
        while time.time() < end_time:
            history = self._loop.run_until_complete(
                self._client.get_messages(entity, limit=1)
            )
            if history and history[0].buttons:
                for row in history[0].buttons:
                    for button in row:
                        if expected_n in _normalize(button.text or ""):
                            self._loop.run_until_complete(button.click())
                            rf_logger.info(f"🖱️ Botão '{button_text}' clicado")
                            return
            time.sleep(1)
        raise AssertionError(f"Botão '{button_text}' não encontrado em {timeout}s")

    def wait_for_reply_containing(self, expected: str, timeout: int = DEFAULT_TIMEOUT):
        """
        Espera até *timeout* s por mensagem contendo *expected*.
        Funciona mesmo quando o bot **edita** a mesma mensagem (texto muda, id permanece).
        """
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
            raise RuntimeError("Conexão não iniciada: use keyword `Open Connection`")
