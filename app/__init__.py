"""
Aplicação Flask Hello World API
Arquitetura em camadas para melhor organização e manutenibilidade
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    
    # Registrar blueprints
    from app.controllers.main_controller import main_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.api_key_controller import api_key_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(api_key_bp, url_prefix='/api')
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app
