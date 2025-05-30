"""
Mensagens para o sistema de configurações
"""

class SettingsMessages:
    """Formatador de mensagens de configurações"""
    
    @staticmethod
    def settings_menu_message(user_name: str, has_code: bool) -> str:
        """Menu principal de configurações"""
        
        status_code = "✅ **Configurado**" if has_code else "❌ **Não configurado**"
        
        return f"""⚙️ **Configurações - {user_name}**

🔐 **Código de Acesso Web:** {status_code}

O código de acesso permite que você faça login na versão web do GEDIE para visualizar relatórios detalhados e gráficos.

**Escolha uma opção:**"""
    
    @staticmethod
    def code_generated_message(code: str) -> str:
        """Código gerado com sucesso"""
        return f"""🎉 **Código de Acesso Gerado!**

🔑 **Seu código:** `{code}`

✅ **Como usar:**
1. Acesse a versão web do GEDIE
2. Digite seu ID do Telegram: Use o comando /id para descobrir
3. Digite este código de 6 dígitos
4. Pronto! Tenha acesso completo aos seus dados

⚠️ **Importante:**
• Guarde este código em local seguro
• O código é pessoal e intransferível
• Você pode regenerar quando quiser

**🌐 Link da versão web:** `http://localhost:5000`"""
    
    @staticmethod
    def current_code_message(code: str) -> str:
        """Mostrar código atual"""
        return f"""🔐 **Seu Código de Acesso Atual**

🔑 **Código:** `{code}`

✅ **Status:** Ativo e funcionando

🌐 **Para acessar a versão web:**
1. Vá para: `http://localhost:5000`
2. Use seu ID do Telegram
3. Digite este código

**Escolha uma ação:**"""
    
    @staticmethod
    def code_regenerated_message(new_code: str) -> str:
        """Código regenerado"""
        return f"""🔄 **Código Regenerado!**

🔑 **Novo código:** `{new_code}`

✅ O código anterior foi invalidado
✅ Use este novo código para acessar a web

⚠️ **Atenção:** Se você estava logado na versão web, precisará fazer login novamente com o novo código.

**🌐 Acesse:** `http://localhost:5000`"""
    
    @staticmethod
    def no_code_message() -> str:
        """Usuário sem código"""
        return f"""🔐 **Código de Acesso**

❌ **Você ainda não possui um código de acesso**

O código permite acesso à versão web do GEDIE, onde você pode:
• 📊 Ver gráficos detalhados de gastos
• 📈 Analisar relatórios avançados
• 🗂️ Gerenciar categorias
• 📱 Sincronizar dados com o Telegram

**Gerar código agora?**"""
    
    @staticmethod
    def id_help_message(telegram_id: int) -> str:
        """Ajuda sobre ID do Telegram"""
        return f"""🆔 **Seu ID do Telegram**

**ID:** `{telegram_id}`

ℹ️ **Este é seu identificador único no Telegram.**

✅ **Como usar:**
1. Copie este número: `{telegram_id}`
2. Acesse a versão web do GEDIE
3. Cole este ID no campo "ID do Telegram"
4. Digite seu código de acesso de 6 dígitos

**🌐 Versão web:** `http://localhost:5000`"""