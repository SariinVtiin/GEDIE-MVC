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
    'host': 'maglev.proxy.rlwy.net',
    'port': 37354,
    'user': 'root',
    'password': 'ZIaAQSYzODTZyRnaSSOcPAYtAgYMSDkH',
    'database': 'railway',
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
    """Dashboard principal com listagem de despesas"""
    expenses = DatabaseManager.execute_query(
        """
        SELECT e.id, e.valor, e.descricao, e.data_gasto, c.nome AS categoria
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = %s
        ORDER BY e.data_gasto DESC
        """,
        (session['user_id'],),
        fetch='all'
    )

    categories = DatabaseManager.execute_query(
    "SELECT nome FROM categories WHERE user_id = %s AND tipo = 'DESPESA' AND ativo = 1",
    (session['user_id'],),
    fetch='all'
    )

    return render_template('dashboard.html', user_name=session.get('user_name'), expenses=expenses, categories=categories)

@app.route('/api/test-db')
def test_db():
    """Endpoint para testar conexão com banco"""
    connection = DatabaseManager.get_connection()
    if connection:
        connection.close()
        return jsonify({'status': 'success', 'message': 'Conexão com banco OK'})
    return jsonify({'status': 'error', 'message': 'Falha na conexão'})

@app.route('/api/categories')
@login_required
def get_categories():
    """Listar categorias do tipo DESPESA para o usuário"""
    categories = DatabaseManager.execute_query(
        "SELECT id, nome FROM categories WHERE user_id = %s AND tipo = 'DESPESA' AND ativo = 1",
        (session['user_id'],),
        fetch='all'
    )
    return jsonify({'categories': categories})

@app.route('/add-expense', methods=['POST'])
@login_required
def add_expense():
    """Adicionar nova despesa"""
    valor = request.form.get('valor')
    descricao = request.form.get('descricao')
    data_gasto = request.form.get('data_gasto')
    category_id = request.form.get('category_id')

    if not all([valor, descricao, data_gasto, category_id]):
        return jsonify({'status': 'error', 'message': 'Todos os campos são obrigatórios.'})

    try:
        DatabaseManager.execute_query(
            """
            INSERT INTO expenses (valor, descricao, data_gasto, category_id, user_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """,
            (valor, descricao, data_gasto, category_id, session['user_id'])
        )
        return jsonify({'status': 'success', 'message': 'Despesa adicionada com sucesso!'})
    except Exception as e:
        print(f"Erro ao adicionar despesa: {e}")
        return jsonify({'status': 'error', 'message': 'Erro ao salvar a despesa.'})

@app.route('/update-expense', methods=['POST'])
@login_required
def update_expense():
    expense_id = request.form.get('id')
    descricao = request.form.get('descricao')
    data_gasto = request.form.get('data_gasto')
    categoria = request.form.get('categoria')
    novo_valor = request.form.get('novo_valor')

    if not all([expense_id, descricao, data_gasto, categoria, novo_valor]):
        return jsonify({'status': 'error', 'message': 'Dados incompletos'})

    try:
        # Buscar o ID da categoria selecionada
        categoria_info = DatabaseManager.execute_query(
            "SELECT id FROM categories WHERE nome = %s AND user_id = %s",
            (categoria, session['user_id']),
            fetch='one'
        )
        if not categoria_info:
            return jsonify({'status': 'error', 'message': 'Categoria inválida'})

        DatabaseManager.execute_query(
            """
            UPDATE expenses
            SET descricao = %s,
                data_gasto = %s,
                valor = %s,
                category_id = %s,
                updated_at = NOW()
            WHERE id = %s AND user_id = %s
            """,
            (descricao, data_gasto, novo_valor, categoria_info['id'], expense_id, session['user_id'])
        )

        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Erro ao atualizar despesa: {e}")
        return jsonify({'status': 'error', 'message': 'Erro ao atualizar a despesa'})

@app.route('/api/expenses')
@login_required
def api_expenses():
    """Retorna todas as despesas do usuário logado"""
    expenses = DatabaseManager.execute_query(
        """
        SELECT e.id, e.valor, e.descricao, e.data_gasto, c.nome AS categoria
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = %s
        ORDER BY e.data_gasto DESC
        """,
        (session['user_id'],),
        fetch='all'
    )
    return jsonify({'expenses': expenses})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)