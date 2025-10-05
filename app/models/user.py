"""
Modelo User - Define a entidade usuário no banco de dados
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """Modelo de usuário com campos básicos e autenticação"""
    
    __tablename__ = 'users'
    
    # Campos da tabela
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """Representação string do objeto"""
        return f'<User {self.name}>'
    
    def set_password(self, password):
        """Define a senha do usuário com hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        """Converte o objeto para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
            
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Cria um objeto User a partir de um dicionário"""
        user = cls(
            name=data.get('name'),
            email=data.get('email'),
            is_active=data.get('is_active', True)
        )
        
        # Definir senha se fornecida
        if 'password' in data:
            user.set_password(data['password'])
        
        return user
    
    def update_from_dict(self, data):
        """Atualiza o objeto User a partir de um dicionário"""
        if 'name' in data:
            self.name = data['name']
        if 'email' in data:
            self.email = data['email']
        if 'is_active' in data:
            self.is_active = data['is_active']
        if 'password' in data:
            self.set_password(data['password'])
        
        # Atualizar timestamp
        self.updated_at = datetime.utcnow()
    
    @staticmethod
    def validate_data(data, required_fields=None, include_password=False):
        """Valida os dados de entrada"""
        if required_fields is None:
            required_fields = ['name', 'email']
        
        if include_password:
            required_fields.append('password')
        
        for field in required_fields:
            if not data.get(field):
                return False, f'Campo {field} é obrigatório'
        
        # Validação básica de email
        if '@' not in data.get('email', ''):
            return False, 'Email inválido'
        
        # Validação de senha
        if include_password and 'password' in data:
            password = data['password']
            if len(password) < 6:
                return False, 'Senha deve ter pelo menos 6 caracteres'
        
        return True, None
