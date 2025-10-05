"""
Serviço de Role - Contém a lógica de negócio para operações com roles
"""
from typing import List, Tuple, Optional
from app.models.role import Role
from app.models.user import User
from app.models.user import user_roles
from app import db

class RoleService:
    """Serviço responsável pelas operações de roles"""
    
    @staticmethod
    def get_all_roles() -> List[Role]:
        """Retorna todos os roles"""
        return Role.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_role_by_id(role_id: int) -> Optional[Role]:
        """Busca um role por ID"""
        return Role.query.get(role_id)
    
    @staticmethod
    def get_role_by_name(role_name: str) -> Optional[Role]:
        """Busca um role por nome"""
        return Role.query.filter_by(name=role_name, is_active=True).first()
    
    @staticmethod
    def create_role(role_data: dict) -> Tuple[Role, bool, str]:
        """
        Cria um novo role
        
        Returns:
            Tuple[Role, bool, str]: (role, sucesso, mensagem)
        """
        # Validar dados
        is_valid, error_message = Role.validate_data(role_data)
        if not is_valid:
            return None, False, error_message
        
        # Verificar se nome já existe
        existing_role = RoleService.get_role_by_name(role_data['name'])
        if existing_role:
            return None, False, 'Nome do role já existe'
        
        try:
            # Criar role
            role = Role.from_dict(role_data)
            db.session.add(role)
            db.session.commit()
            
            return role, True, 'Role criado com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return None, False, f'Erro ao criar role: {str(e)}'
    
    @staticmethod
    def update_role(role_id: int, role_data: dict) -> Tuple[Optional[Role], bool, str]:
        """
        Atualiza um role existente
        
        Returns:
            Tuple[Optional[Role], bool, str]: (role, sucesso, mensagem)
        """
        role = RoleService.get_role_by_id(role_id)
        if not role:
            return None, False, 'Role não encontrado'
        
        # Verificar se nome já existe em outro role
        if 'name' in role_data and role_data['name'] != role.name:
            existing_role = RoleService.get_role_by_name(role_data['name'])
            if existing_role:
                return None, False, 'Nome do role já existe'
        
        try:
            # Atualizar role
            role.update_from_dict(role_data)
            db.session.commit()
            
            return role, True, 'Role atualizado com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return None, False, f'Erro ao atualizar role: {str(e)}'
    
    @staticmethod
    def delete_role(role_id: int) -> Tuple[bool, str]:
        """
        Deleta um role (soft delete)
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        role = RoleService.get_role_by_id(role_id)
        if not role:
            return False, 'Role não encontrado'
        
        try:
            # Soft delete - desativar role
            role.is_active = False
            db.session.commit()
            
            return True, 'Role deletado com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return False, f'Erro ao deletar role: {str(e)}'
    
    @staticmethod
    def assign_role_to_user(user_id: int, role_id: int, assigned_by: int = None) -> Tuple[bool, str]:
        """
        Atribui um role a um usuário
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        user = User.query.get(user_id)
        role = Role.query.get(role_id)
        
        if not user:
            return False, 'Usuário não encontrado'
        
        if not role:
            return False, 'Role não encontrado'
        
        if not role.is_active:
            return False, 'Role não está ativo'
        
        # Verificar se já tem o role
        if user.has_role(role.name):
            return False, 'Usuário já possui este role'
        
        try:
            # Adicionar role ao usuário
            user.add_role(role)
            
            # Registrar na tabela user_roles
            db.session.execute(
                user_roles.insert().values(
                    user_id=user_id,
                    role_id=role_id,
                    assigned_by=assigned_by
                )
            )
            db.session.commit()
            
            return True, 'Role atribuído com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return False, f'Erro ao atribuir role: {str(e)}'
    
    @staticmethod
    def remove_role_from_user(user_id: int, role_id: int) -> Tuple[bool, str]:
        """
        Remove um role de um usuário
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        user = User.query.get(user_id)
        role = Role.query.get(role_id)
        
        if not user:
            return False, 'Usuário não encontrado'
        
        if not role:
            return False, 'Role não encontrado'
        
        # Verificar se tem o role
        if not user.has_role(role.name):
            return False, 'Usuário não possui este role'
        
        try:
            # Remover role do usuário
            user.remove_role(role)
            
            # Desativar na tabela user_roles
            db.session.execute(
                user_roles.update().where(
                    (user_roles.c.user_id == user_id) & 
                    (user_roles.c.role_id == role_id)
                ).values(is_active=False)
            )
            db.session.commit()
            
            return True, 'Role removido com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return False, f'Erro ao remover role: {str(e)}'
    
    @staticmethod
    def get_user_roles(user_id: int) -> List[Role]:
        """Retorna todos os roles de um usuário"""
        user = User.query.get(user_id)
        if not user:
            return []
        
        return [role for role in user.roles if role.is_active]
    
    @staticmethod
    def get_role_users(role_id: int) -> List[User]:
        """Retorna todos os usuários de um role"""
        role = Role.query.get(role_id)
        if not role:
            return []
        
        return [user for user in role.users if user.is_active]
    
    @staticmethod
    def initialize_default_roles() -> Tuple[bool, str]:
        """
        Inicializa os roles padrão do sistema
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            default_roles = Role.get_default_roles()
            
            for role_data in default_roles:
                existing_role = RoleService.get_role_by_name(role_data['name'])
                if not existing_role:
                    role, success, message = RoleService.create_role(role_data)
                    if not success:
                        return False, f'Erro ao criar role {role_data["name"]}: {message}'
            
            return True, 'Roles padrão inicializados com sucesso'
        
        except Exception as e:
            return False, f'Erro ao inicializar roles padrão: {str(e)}'
    
    @staticmethod
    def get_roles_count() -> int:
        """Retorna o total de roles ativos"""
        return Role.query.filter_by(is_active=True).count()
