"""
Modelo Role - Define os roles/perfis de usuário no sistema
"""
from datetime import datetime
from app import db
from .user import user_roles

class Role(db.Model):
    """Modelo de Role para controle de acesso baseado em papéis"""
    
    __tablename__ = 'roles'
    
    # Campos da tabela
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    permissions = db.Column(db.JSON, default=list)  # Lista de permissões
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com usuários (many-to-many)
    users = db.relationship('User', secondary=user_roles, back_populates='roles', primaryjoin='Role.id == user_roles.c.role_id', secondaryjoin='User.id == user_roles.c.user_id')
    
    def __repr__(self):
        """Representação string do objeto"""
        return f'<Role {self.name}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'permissions': self.permissions,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Role a partir de um dicionário"""
        return cls(
            name=data.get('name'),
            display_name=data.get('display_name'),
            description=data.get('description'),
            permissions=data.get('permissions', []),
            is_active=data.get('is_active', True)
        )
    
    def update_from_dict(self, data):
        """Atualiza o objeto Role a partir de um dicionário"""
        if 'name' in data:
            self.name = data['name']
        if 'display_name' in data:
            self.display_name = data['display_name']
        if 'description' in data:
            self.description = data['description']
        if 'permissions' in data:
            self.permissions = data['permissions']
        if 'is_active' in data:
            self.is_active = data['is_active']
        
        # Atualizar timestamp
        self.updated_at = datetime.utcnow()
    
    def has_permission(self, permission):
        """Verifica se o role tem uma permissão específica"""
        return permission in self.permissions
    
    def add_permission(self, permission):
        """Adiciona uma permissão ao role"""
        if permission not in self.permissions:
            self.permissions.append(permission)
            self.updated_at = datetime.utcnow()
    
    def remove_permission(self, permission):
        """Remove uma permissão do role"""
        if permission in self.permissions:
            self.permissions.remove(permission)
            self.updated_at = datetime.utcnow()
    
    @staticmethod
    def validate_data(data, required_fields=None):
        """Valida os dados de entrada"""
        if required_fields is None:
            required_fields = ['name', 'display_name']
        
        for field in required_fields:
            if not data.get(field):
                return False, f'Campo {field} é obrigatório'
        
        # Validação básica de name (deve ser único e em lowercase)
        if 'name' in data:
            name = data['name'].lower().replace(' ', '_')
            if not name.replace('_', '').isalnum():
                return False, 'Nome do role deve conter apenas letras, números e underscores'
        
        return True, None
    
    @classmethod
    def get_default_roles(cls):
        """Retorna os roles padrão do sistema"""
        return [
            {
                'name': 'admin',
                'display_name': 'Administrador',
                'description': 'Acesso total ao sistema',
                'permissions': [
                    'users:read', 'users:write', 'users:delete',
                    'api_keys:read', 'api_keys:write', 'api_keys:delete',
                    'roles:read', 'roles:write', 'roles:delete',
                    'system:admin'
                ]
            },
            {
                'name': 'client',
                'display_name': 'Cliente',
                'description': 'Usuário padrão do sistema',
                'permissions': [
                    'users:read_own', 'users:write_own',
                    'api_keys:read_own', 'api_keys:write_own', 'api_keys:delete_own'
                ]
            }
        ]
