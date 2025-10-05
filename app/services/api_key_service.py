"""
Serviço de API Key - Contém a lógica de negócio para operações com API Keys
"""
from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from app.models.api_key import ApiKey
from app import db

class ApiKeyService:
    """Serviço responsável pelas operações de API Key"""
    
    @staticmethod
    def get_all_api_keys() -> List[ApiKey]:
        """Retorna todas as API Keys"""
        return ApiKey.query.all()
    
    @staticmethod
    def get_api_key_by_id(api_key_id: int) -> Optional[ApiKey]:
        """Busca uma API Key por ID"""
        return ApiKey.query.get(api_key_id)
    
    @staticmethod
    def get_api_key_by_key(api_key: str) -> Optional[ApiKey]:
        """Busca uma API Key pelo valor da chave"""
        key_hash = ApiKey.hash_key(api_key)
        return ApiKey.query.filter_by(key_hash=key_hash).first()
    
    @staticmethod
    def get_user_api_keys(user_id: int) -> List[ApiKey]:
        """Busca todas as API Keys de um usuário"""
        return ApiKey.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def create_api_key(api_key_data: dict) -> Tuple[ApiKey, bool, str]:
        """
        Cria uma nova API Key
        
        Returns:
            Tuple[ApiKey, bool, str]: (api_key, sucesso, mensagem)
        """
        # Validar dados
        is_valid, error_message = ApiKey.validate_data(api_key_data)
        if not is_valid:
            return None, False, error_message
        
        try:
            # Criar API Key
            api_key = ApiKey.from_dict(api_key_data)
            db.session.add(api_key)
            db.session.commit()
            
            return api_key, True, 'API Key criada com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return None, False, f'Erro ao criar API Key: {str(e)}'
    
    @staticmethod
    def update_api_key(api_key_id: int, api_key_data: dict) -> Tuple[Optional[ApiKey], bool, str]:
        """
        Atualiza uma API Key existente
        
        Returns:
            Tuple[Optional[ApiKey], bool, str]: (api_key, sucesso, mensagem)
        """
        api_key = ApiKeyService.get_api_key_by_id(api_key_id)
        if not api_key:
            return None, False, 'API Key não encontrada'
        
        try:
            # Atualizar API Key
            api_key.update_from_dict(api_key_data)
            db.session.commit()
            
            return api_key, True, 'API Key atualizada com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return None, False, f'Erro ao atualizar API Key: {str(e)}'
    
    @staticmethod
    def delete_api_key(api_key_id: int) -> Tuple[bool, str]:
        """
        Deleta uma API Key
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        api_key = ApiKeyService.get_api_key_by_id(api_key_id)
        if not api_key:
            return False, 'API Key não encontrada'
        
        try:
            db.session.delete(api_key)
            db.session.commit()
            
            return True, 'API Key deletada com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return False, f'Erro ao deletar API Key: {str(e)}'
    
    @staticmethod
    def deactivate_api_key(api_key_id: int) -> Tuple[bool, str]:
        """
        Desativa uma API Key
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        api_key = ApiKeyService.get_api_key_by_id(api_key_id)
        if not api_key:
            return False, 'API Key não encontrada'
        
        try:
            api_key.is_active = False
            db.session.commit()
            
            return True, 'API Key desativada com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return False, f'Erro ao desativar API Key: {str(e)}'
    
    @staticmethod
    def activate_api_key(api_key_id: int) -> Tuple[bool, str]:
        """
        Ativa uma API Key
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        api_key = ApiKeyService.get_api_key_by_id(api_key_id)
        if not api_key:
            return False, 'API Key não encontrada'
        
        try:
            api_key.is_active = True
            db.session.commit()
            
            return True, 'API Key ativada com sucesso'
        
        except Exception as e:
            db.session.rollback()
            return False, f'Erro ao ativar API Key: {str(e)}'
    
    @staticmethod
    def validate_api_key(api_key: str) -> Tuple[Optional[ApiKey], bool, str]:
        """
        Valida uma API Key
        
        Returns:
            Tuple[Optional[ApiKey], bool, str]: (api_key, válida, mensagem)
        """
        if not api_key:
            return None, False, 'API Key é obrigatória'
        
        # Buscar API Key
        api_key_obj = ApiKeyService.get_api_key_by_key(api_key)
        if not api_key_obj:
            return None, False, 'API Key inválida'
        
        # Verificar se está ativa
        if not api_key_obj.is_active:
            return None, False, 'API Key desativada'
        
        # Verificar se não expirou
        if api_key_obj.is_expired():
            return None, False, 'API Key expirada'
        
        # Atualizar último uso
        api_key_obj.update_last_used()
        
        return api_key_obj, True, 'API Key válida'
    
    @staticmethod
    def get_api_keys_count() -> int:
        """Retorna o total de API Keys"""
        return ApiKey.query.count()
    
    @staticmethod
    def get_active_api_keys_count() -> int:
        """Retorna o total de API Keys ativas"""
        return ApiKey.query.filter_by(is_active=True).count()
