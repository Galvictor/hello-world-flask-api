"""
Serviço de usuário - Contém a lógica de negócio para operações com usuários
"""
from typing import List, Tuple, Optional
from app.models.user import User
from app import db

class UserService:
    """Serviço responsável pelas operações de usuário"""
    
    @staticmethod
    def get_all_users() -> List[User]:
        """Retorna todos os usuários"""
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Busca um usuário por ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Busca um usuário por email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_user(user_data: dict) -> Tuple[User, bool, str]:
        """
        Cria um novo usuário
        
        Returns:
            Tuple[User, bool, str]: (usuário, sucesso, mensagem)
        """
        # Validar dados incluindo senha
        is_valid, error_message = User.validate_data(user_data, include_password=True)
        if not is_valid:
            return None, False, error_message
        
        # Verificar se email já existe
        existing_user = UserService.get_user_by_email(user_data['email'])
        if existing_user:
            return None, False, 'Email já cadastrado'
        
        try:
            # Criar usuário
            user = User.from_dict(user_data)
            db.session.add(user)
            db.session.commit()
            
            # Atribuir role 'client' automaticamente a novos usuários
            from app.services.role_service import RoleService
            client_role = RoleService.get_role_by_name('client')
            if client_role:
                user.add_role(client_role)
                print(f"Role 'client' atribuído automaticamente ao usuário {user.email}")
            else:
                print(f"AVISO: Role 'client' não encontrado para o usuário {user.email}")
            
            return user, True, 'Usuário criado com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return None, False, f'Erro ao criar usuário: {str(e)}'
    
    @staticmethod
    def update_user(user_id: int, user_data: dict) -> Tuple[Optional[User], bool, str]:
        """
        Atualiza um usuário existente
        
        Returns:
            Tuple[Optional[User], bool, str]: (usuário, sucesso, mensagem)
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None, False, 'Usuário não encontrado'
        
        # Verificar se email já existe em outro usuário
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = UserService.get_user_by_email(user_data['email'])
            if existing_user:
                return None, False, 'Email já cadastrado'
        
        try:
            # Atualizar usuário
            user.update_from_dict(user_data)
            db.session.commit()
            
            return user, True, 'Usuário atualizado com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return None, False, f'Erro ao atualizar usuário: {str(e)}'
    
    @staticmethod
    def delete_user(user_id: int) -> Tuple[bool, str]:
        """
        Deleta um usuário
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            return False, 'Usuário não encontrado'
        
        try:
            db.session.delete(user)
            db.session.commit()
            
            return True, 'Usuário deletado com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return False, f'Erro ao deletar usuário: {str(e)}'
    
    @staticmethod
    def get_users_count() -> int:
        """Retorna o total de usuários"""
        return User.query.count()
