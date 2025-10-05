"""
Configurações gerais da aplicação
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class AppConfig:
    """Configurações gerais da aplicação Flask"""
    
    # Configurações de segurança
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configurações de desenvolvimento
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')
    
    # Configurações do servidor
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Configurações da API
    API_TITLE = 'Hello World Flask API'
    API_VERSION = '1.0.0'
    API_DESCRIPTION = 'Uma API simples em Flask com SQLite para demonstrar funcionalidades básicas'
    
    # Configurações JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # Configurações API Key
    API_KEY_HEADER_NAME = os.getenv('API_KEY_HEADER_NAME', 'X-API-Key')
    API_KEY_DEFAULT_EXPIRES_DAYS = int(os.getenv('API_KEY_DEFAULT_EXPIRES_DAYS', 365))
