"""
Modelo User - Define a entidade usuário no banco de dados
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# Tabela de relacionamento many-to-many
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow),
    db.Column('assigned_by', db.Integer, db.ForeignKey('users.id'), nullable=True),
    db.Column('is_active', db.Boolean, default=True)
)

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
    
    # Relacionamento com roles (many-to-many)
    roles = db.relationship('Role', secondary=user_roles, back_populates='users', primaryjoin='User.id == user_roles.c.user_id', secondaryjoin='Role.id == user_roles.c.role_id')
    
    def __repr__(self):
        """Representação string do objeto"""
        return f'<User {self.name}>'
    
    def set_password(self, password):
        """Define a senha do usuário com hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False, include_roles=False):
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
        
        if include_roles:
            data['roles'] = [role.to_dict() for role in self.roles if role.is_active]
            data['role_names'] = self.get_role_names()
            data['permissions'] = self.get_all_permissions()
            
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
    
    def has_role(self, role_name):
        """Verifica se o usuário tem um role específico"""
        return any(role.name == role_name for role in self.roles if role.is_active)
    
    def has_permission(self, permission):
        """Verifica se o usuário tem uma permissão específica"""
        for role in self.roles:
            if role.is_active and role.has_permission(permission):
                return True
        return False
    
    def add_role(self, role):
        """Adiciona um role ao usuário"""
        if role not in self.roles:
            self.roles.append(role)
            db.session.commit()
    
    def remove_role(self, role):
        """Remove um role do usuário"""
        if role in self.roles:
            self.roles.remove(role)
            db.session.commit()
    
    def get_role_names(self):
        """Retorna uma lista com os nomes dos roles ativos do usuário"""
        return [role.name for role in self.roles if role.is_active]
    
    def get_all_permissions(self):
        """Retorna todas as permissões do usuário (baseadas nos roles)"""
        permissions = set()
        for role in self.roles:
            if role.is_active:
                permissions.update(role.permissions)
        return list(permissions)
