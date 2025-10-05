"""
Modelo API Key - Define a entidade API Key no banco de dados
"""
from datetime import datetime
from app import db
import secrets
import hashlib

class ApiKey(db.Model):
    """Modelo de API Key para autenticação de serviços"""
    
    __tablename__ = 'api_keys'
    
    # Campos da tabela
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    key_hash = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    last_used_at = db.Column(db.DateTime, nullable=True)
    
    # Relacionamento com usuário
    user = db.relationship('User', backref=db.backref('api_keys', lazy=True))
    
    def __repr__(self):
        """Representação string do objeto"""
        return f'<ApiKey {self.name}>'
    
    @classmethod
    def generate_key(cls):
        """Gera uma nova API Key"""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def hash_key(cls, key):
        """Gera hash da API Key"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def set_key(self, key):
        """Define a API Key com hash"""
        self.key_hash = self.hash_key(key)
    
    def verify_key(self, key):
        """Verifica se a API Key está correta"""
        return self.key_hash == self.hash_key(key)
    
    def is_expired(self):
        """Verifica se a API Key expirou"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        """Verifica se a API Key é válida (ativa e não expirada)"""
        return self.is_active and not self.is_expired()
    
    def update_last_used(self):
        """Atualiza o timestamp de último uso"""
        self.last_used_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self, include_key=False):
        """Converte o objeto para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'is_expired': self.is_expired()
        }
        
        # Só incluir a key se fornecida e for a primeira vez
        if include_key and hasattr(self, '_plain_key'):
            data['key'] = self._plain_key
            
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Cria um objeto ApiKey a partir de um dicionário"""
        api_key = cls(
            name=data.get('name'),
            description=data.get('description'),
            is_active=data.get('is_active', True),
            user_id=data.get('user_id')
        )
        
        # Definir expiração se fornecida
        if 'expires_at' in data and data['expires_at']:
            api_key.expires_at = datetime.fromisoformat(data['expires_at'])
        
        # Gerar e definir a key
        key = cls.generate_key()
        api_key.set_key(key)
        api_key._plain_key = key  # Armazenar temporariamente para retorno
        
        return api_key
    
    def update_from_dict(self, data):
        """Atualiza o objeto ApiKey a partir de um dicionário"""
        if 'name' in data:
            self.name = data['name']
        if 'description' in data:
            self.description = data['description']
        if 'is_active' in data:
            self.is_active = data['is_active']
        if 'expires_at' in data:
            self.expires_at = datetime.fromisoformat(data['expires_at']) if data['expires_at'] else None
    
    @staticmethod
    def validate_data(data, required_fields=None):
        """Valida os dados de entrada"""
        if required_fields is None:
            required_fields = ['name']
        
        for field in required_fields:
            if not data.get(field):
                return False, f'Campo {field} é obrigatório'
        
        return True, None
