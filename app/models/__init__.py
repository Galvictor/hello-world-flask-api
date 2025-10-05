"""
Camada de modelos - Define as entidades do banco de dados
"""

from .user import User
from .api_key import ApiKey

__all__ = ['User', 'ApiKey']
