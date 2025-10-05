"""
Camada de controladores - Define as rotas e endpoints da API
"""

from .main_controller import main_bp
from .user_controller import user_bp
from .auth_controller import auth_bp
from .api_key_controller import api_key_bp

__all__ = ['main_bp', 'user_bp', 'auth_bp', 'api_key_bp']