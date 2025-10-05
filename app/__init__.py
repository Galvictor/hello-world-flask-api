"""
Aplicação Flask Hello World API
Arquitetura em camadas para melhor organização e manutenibilidade
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# Instâncias globais
db = SQLAlchemy()

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    from app.config.database import DatabaseConfig
    from app.config.app import AppConfig
    
    app.config.from_object(DatabaseConfig)
    app.config.from_object(AppConfig)
    
    # Inicializar extensões
    db.init_app(app)
    
    # Configurar Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Hello World Flask API",
            "description": "API REST com autenticação JWT, API Keys e sistema de roles",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
                "email": "admin@system.com"
            }
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT token no formato: Bearer {token}"
            },
            "ApiKey": {
                "type": "apiKey",
                "name": "X-API-Key",
                "in": "header",
                "description": "API Key para autenticação"
            }
        },
        "tags": [
            {
                "name": "Main",
                "description": "Endpoints principais da aplicação"
            },
            {
                "name": "Auth",
                "description": "Autenticação e autorização"
            },
            {
                "name": "Users",
                "description": "Gerenciamento de usuários"
            },
            {
                "name": "API Keys",
                "description": "Gerenciamento de API Keys"
            },
            {
                "name": "Roles",
                "description": "Sistema de roles e permissões"
            }
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Registrar blueprints
    from app.controllers.main_controller import main_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.api_key_controller import api_key_bp
    from app.controllers.role_controller import role_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(api_key_bp, url_prefix='/api')
    app.register_blueprint(role_bp, url_prefix='/api')
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
        
        # Inicializar dados padrão se necessário
        from app.utils.seed_data import initialize_default_data
        initialize_default_data()
    
    return app
