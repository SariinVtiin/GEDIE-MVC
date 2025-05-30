#!/usr/bin/env python3
"""
GEDIE Web Setup Script
Script para configurar e verificar o ambiente da aplicação web
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def print_banner():
    """Exibir banner do GEDIE"""
    print("=" * 60)
    print("🚀 GEDIE - Setup da Aplicação Web")
    print("   Gerenciador de Despesas Inteligente")
    print("=" * 60)
    print()

def check_python_version():
    """Verificar versão do Python"""
    print("📋 Verificando versão do Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} OK")
    return True

def check_mysql_connection():
    """Verificar conexão com MySQL"""
    print("\n🗄️ Verificando conexão com MySQL...")
    
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'gedie_user',
        'password': 'senha_super_segura_123',
        'database': 'gedie_db'
    }
    
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"✅ Conectado ao banco: {db_name}")
            
            # Verificar tabelas
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            
            expected_tables = ['users', 'categories', 'expenses']
            missing_tables = [t for t in expected_tables if t not in table_names]
            
            if missing_tables:
                print(f"⚠️ Tabelas faltando: {', '.join(missing_tables)}")
                return False
            else:
                print(f"✅ Todas as tabelas encontradas: {', '.join(table_names)}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Erro na conexão: {e}")
        print("\n🔧 Soluções possíveis:")
        print("   1. Verificar se o MySQL está rodando")
        print("   2. Verificar credenciais no arquivo app.py")
        print("   3. Criar o banco e usuário se necessário")
        return False

def install_dependencies():
    """Instalar dependências Python"""
    print("\n📦 Instalando dependências...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso!")
            return True
        else:
            print(f"❌ Erro ao instalar dependências: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def create_directories():
    """Criar estrutura de diretórios"""
    print("\n📁 Criando estrutura de diretórios...")
    
    directories = [
        'static',
        'static/css',
        'static/js',
        'static/images',
        'templates',
        'instance',
        'logs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Criado: {directory}/")
        else:
            print(f"   ℹ️  Já existe: {directory}/")

def check_files():
    """Verificar arquivos necessários"""
    print("\n📄 Verificando arquivos...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'static/css/style.css',
        'static/js/login.js',
        'templates/login.html',
        'templates/dashboard.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Arquivos faltando: {len(missing_files)}")
        print("   Certifique-se de copiar todos os arquivos para as pastas corretas")
        return False
    
    return True

def test_flask_app():
    """Testar se a aplicação Flask pode ser importada"""
    print("\n🧪 Testando aplicação Flask...")
    
    try:
        # Tentar importar o app
        sys.path.insert(0, os.getcwd())
        from app import app, DatabaseManager
        
        print("✅ Aplicação Flask carregada com sucesso!")
        
        # Testar conexão com banco via app
        with app.app_context():
            result = DatabaseManager.execute_query("SELECT 1", fetch='one')
            if result:
                print("✅ Conexão com banco via Flask OK!")
                return True
            else:
                print("❌ Erro na conexão com banco via Flask")
                return False
                
    except ImportError as e:
        print(f"❌ Erro ao importar app: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def create_env_file():
    """Criar arquivo .env se não existir"""
    print("\n⚙️ Verificando arquivo de configuração...")
    
    if not os.path.exists('.env'):
        print("   Criando arquivo .env...")
        env_content = """# GEDIE Web Application - Environment Variables
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=gedie_secret_key_2024_change_in_production

# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=gedie_user
MYSQL_PASSWORD=senha_super_segura_123
MYSQL_DATABASE=gedie_db
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("   ✅ Arquivo .env criado!")
    else:
        print("   ℹ️  Arquivo .env já existe")

def main():
    """Função principal do setup"""
    print_banner()
    
    # Lista de verificações
    checks = [
        ("Versão Python", check_python_version),
        ("Estrutura de diretórios", create_directories),
        ("Arquivo de configuração", create_env_file),
        ("Arquivos necessários", check_files),
        ("Dependências Python", install_dependencies),
        ("Conexão MySQL", check_mysql_connection),
        ("Aplicação Flask", test_flask_app)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erro em '{name}': {e}")
            results.append((name, False))
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DO SETUP")
    print("=" * 60)
    
    success_count = 0
    for name, success in results:
        status = "✅ OK" if success else "❌ ERRO"
        print(f"{status:<8} {name}")
        if success:
            success_count += 1
    
    print(f"\nResultado: {success_count}/{len(results)} verificações passaram")
    
    if success_count == len(results):
        print("\n🎉 SETUP CONCLUÍDO COM SUCESSO!")
        print("\n🚀 Para iniciar a aplicação:")
        print("   python app.py")
        print("\n🌐 Acesse: http://localhost:5000")
        print("\n🔑 Login de teste:")
        print("   Telegram ID: 6212796124")
        print("   Código: 123456")
    else:
        print("\n⚠️ SETUP INCOMPLETO")
        print("   Corrija os erros acima antes de continuar")
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()