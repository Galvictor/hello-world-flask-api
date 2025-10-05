"""
Controlador principal - Endpoints gerais da API
"""
from flask import Blueprint, jsonify
from app.config.app import AppConfig

# Criar blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def hello_world():
    """
    Endpoint principal da API
    ---
    tags:
      - Main
    summary: Mensagem de boas-vindas
    description: Retorna uma mensagem de Hello World e informações básicas da API
    responses:
      200:
        description: Mensagem de boas-vindas
        schema:
          type: object
          properties:
            message:
              type: string
              example: Hello, World!
            status:
              type: string
              example: success
            api:
              type: string
              example: Flask API com SQLite - Arquitetura em Camadas
    """
    return jsonify({
        'message': 'Hello, World!',
        'status': 'success',
        'api': 'Flask API com SQLite - Arquitetura em Camadas'
    })

@main_bp.route('/health')
def health_check():
    """
    Verificação de saúde da API
    ---
    tags:
      - Main
    summary: Status da aplicação
    description: Verifica se a API está funcionando corretamente
    responses:
      200:
        description: API funcionando corretamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            message:
              type: string
              example: API está funcionando corretamente
            database:
              type: string
              example: SQLite conectado
            architecture:
              type: string
              example: Layered Architecture
    """
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
