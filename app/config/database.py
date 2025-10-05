"""
Configurações do banco de dados
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class DatabaseConfig:
    """Configurações do banco de dados"""
    
    # Configurações básicas do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Configuração da URL do banco baseada na variável de ambiente
    @staticmethod
    def get_database_url():
        """Retorna a URL do banco baseada na configuração"""
        database_type = os.getenv('DATABASE_TYPE', 'sqlite')
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            return database_url
        
        # Fallback para SQLite se não especificado
        if database_type.lower() == 'sqlite':
            basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            return f'sqlite:///{os.path.join(basedir, "database.db")}'
        
        # Para outros tipos de banco, usar DATABASE_URL
        raise ValueError(f"Para {database_type}, configure DATABASE_URL no arquivo .env")
    
    # Propriedade para a URL do banco
    SQLALCHEMY_DATABASE_URI = get_database_url()
