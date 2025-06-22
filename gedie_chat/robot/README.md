# Telegram Bot Functional Tests (Robot Framework)

Este projeto contém uma suíte completa de testes End‑to‑End em **Robot Framework** para o bot **GEDIE** no Telegram.

| Recurso                   | Descrição                                                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `libs/TelegramLibrary.py` | Biblioteca customizada usando **Telethon** para interagir com o bot como se fosse um usuário real (envia mensagens, clica em botões, aguarda respostas). |
| `resources/`              | Variáveis e _keywords_ reusáveis em linguagem _BDD_ 🇧🇷 (`Dado`, `Quando`, `Então`, `E`).                                                                 |
| `tests/`                  | Suítes organizadas por finalidade (_smoke_, _flows_, _regression_). Cada caso simula cenários de uso reais do GEDIE.                                     |
| `.env.template`           | Exemplo de variáveis de ambiente necessárias para executar os testes sem expor credenciais.                                                              |
| `requirements.txt`        | Dependências Python.                                                                                                                                     |

## 📦 Instalação

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Execução local

```bash
robot -d results tests
```

## 🔐 Variáveis Sensíveis

Todas as credenciais são lidas a partir de variáveis de ambiente seguindo 12‑factor. **Nunca** suba `.env` real ao Git.

| Variável          | Exemplo          | Descrição                                          |
| ----------------- | ---------------- | -------------------------------------------------- |
| `TG_API_ID`       | `123456`         | API ID obtido em https://my.telegram.org           |
| `TG_API_HASH`     | `abcd1234...`    | API Hash                                           |
| `TG_PHONE`        | `+5511999999999` | Telefone da conta de teste (formato internacional) |
| `TG_BOT_USERNAME` | `@gedie_bot`     | Username público do bot a ser testado              |
