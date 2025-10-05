"""
Controlador principal - Endpoints gerais da API
"""
from flask import Blueprint, jsonify
from app.config.app import AppConfig

# Criar blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def hello_world():
    """Endpoint principal que retorna uma mensagem de Hello World"""
    return jsonify({
        'message': 'Hello, World!',
        'status': 'success',
        'api': 'Flask API com SQLite - Arquitetura em Camadas'
    })

@main_bp.route('/health')
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'healthy',
        'message': 'API está funcionando corretamente',
        'database': 'SQLite conectado',
        'architecture': 'Layered Architecture'
    })

@main_bp.route('/info')
def api_info():
    """Endpoint que retorna informações sobre a API"""
    return jsonify({
        'name': AppConfig.API_TITLE,
        'version': AppConfig.API_VERSION,
        'description': AppConfig.API_DESCRIPTION,
        'database': 'SQLite',
        'architecture': 'Layered Architecture (Models, Services, Controllers)',
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Mensagem de boas-vindas'},
            {'path': '/health', 'method': 'GET', 'description': 'Verificação de saúde da API'},
            {'path': '/info', 'method': 'GET', 'description': 'Informações sobre a API'},
            {'path': '/api/users', 'method': 'GET', 'description': 'Listar todos os usuários'},
            {'path': '/api/users', 'method': 'POST', 'description': 'Criar novo usuário'},
            {'path': '/api/users/<id>', 'method': 'GET', 'description': 'Buscar usuário por ID'},
            {'path': '/api/users/<id>', 'method': 'PUT', 'description': 'Atualizar usuário'},
            {'path': '/api/users/<id>', 'method': 'DELETE', 'description': 'Deletar usuário'}
        ]
    })
