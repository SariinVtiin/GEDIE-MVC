#!/usr/bin/env python3
"""
GEDIE Web Application
Sistema de Gestão de Despesas Inteligente - Frontend Web
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'gedie_secret_key_2024'  # Em produção, usar variável de ambiente

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'gedie_user',
    'password': 'senha_super_segura_123',
    'database': 'gedie_db',
    'charset': 'utf8mb4'
}

class DatabaseManager:
    """Gerenciador de conexões com o banco de dados"""
    
    @staticmethod
    def get_connection():
        """Criar conexão com o banco"""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            return connection
        except Error as e:
            print(f"Erro ao conectar com MySQL: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """Executar query no banco"""
        connection = DatabaseManager.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall() if fetch == 'all' else cursor.fetchone()
            else:
                connection.commit()
                result = cursor.rowcount
            
            return result
        except Error as e:
            print(f"Erro ao executar query: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

def login_required(f):
    """Decorator para rotas que requerem login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Página inicial - redireciona para login ou dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        telegram_id = request.form.get('telegram_id')
        access_code = request.form.get('access_code')
        
        if not telegram_id or not access_code:
            flash('Por favor, preencha todos os campos', 'error')
            return render_template('login.html')
        
        # Validar formato dos dados
        if not telegram_id.isdigit():
            flash('ID do Telegram deve conter apenas números', 'error')
            return render_template('login.html')
        
        if len(access_code) != 6 or not access_code.isdigit():
            flash('Código de acesso deve ter exatamente 6 dígitos', 'error')
            return render_template('login.html')
        
        # Buscar usuário pelo telegram_id e código
        user = DatabaseManager.execute_query(
            "SELECT * FROM users WHERE telegram_id = %s AND codigo_acesso = %s AND ativo = 1",
            (telegram_id, access_code),
            fetch='one'
        )
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['nome']
            session['telegram_id'] = user['telegram_id']
            
            flash(f'Bem-vindo, {user["nome"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('ID do Telegram ou código de acesso incorretos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    return render_template('dashboard.html', user_name=session.get('user_name'))

@app.route('/api/test-db')
def test_db():
    """Endpoint para testar conexão com banco"""
    connection = DatabaseManager.get_connection()
    if connection:
        connection.close()
        return jsonify({'status': 'success', 'message': 'Conexão com banco OK'})
    return jsonify({'status': 'error', 'message': 'Falha na conexão'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)