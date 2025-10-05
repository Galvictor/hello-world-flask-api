"""
Controlador de API Key - Endpoints relacionados às API Keys
"""
from flask import Blueprint, jsonify, request
from app.services.api_key_service import ApiKeyService
from app.utils.auth_decorators import admin_required, token_required
from app.utils.response_utils import ResponseUtils

# Criar blueprint
api_key_bp = Blueprint('api_keys', __name__)

@api_key_bp.route('/api-keys', methods=['GET'])
@admin_required
def get_api_keys(current_user):
    """Listar todas as API Keys (requer privilégios de admin)"""
    try:
        api_keys = ApiKeyService.get_all_api_keys()
        api_keys_data = [api_key.to_dict() for api_key in api_keys]
        total = ApiKeyService.get_api_keys_count()
        active_count = ApiKeyService.get_active_api_keys_count()
        
        return ResponseUtils.success_response(
            data={
                'api_keys': api_keys_data,
                'total': total,
                'active_count': active_count
            },
            message='API Keys listadas com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@api_key_bp.route('/api-keys', methods=['POST'])
@admin_required
def create_api_key(current_user):
    """Criar nova API Key (requer privilégios de admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        # Adicionar user_id se não fornecido
        if 'user_id' not in data:
            data['user_id'] = current_user.id
        
        api_key, success, message = ApiKeyService.create_api_key(data)
        
        if success:
            return ResponseUtils.success_response(
                data={
                    'api_key': api_key.to_dict(include_key=True)
                },
                message=message,
                status_code=201
            )
        else:
            return ResponseUtils.error_response(message, status_code=400)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@api_key_bp.route('/api-keys/<int:api_key_id>', methods=['GET'])
@admin_required
def get_api_key(current_user, api_key_id):
    """Buscar API Key por ID (requer privilégios de admin)"""
    try:
        api_key = ApiKeyService.get_api_key_by_id(api_key_id)
        
        if not api_key:
            return ResponseUtils.error_response(
                'API Key não encontrada',
                status_code=404
            )
        
        return ResponseUtils.success_response(
            data={'api_key': api_key.to_dict()},
            message='API Key encontrada com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@api_key_bp.route('/api-keys/<int:api_key_id>', methods=['PUT'])
@admin_required
def update_api_key(current_user, api_key_id):
    """Atualizar API Key (requer privilégios de admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        api_key, success, message = ApiKeyService.update_api_key(api_key_id, data)
        
        if success:
            return ResponseUtils.success_response(
                data={'api_key': api_key.to_dict()},
                message=message
            )
        else:
            status_code = 404 if 'não encontrada' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@api_key_bp.route('/api-keys/<int:api_key_id>', methods=['DELETE'])
@admin_required
def delete_api_key(current_user, api_key_id):
    """Deletar API Key (requer privilégios de admin)"""
    try:
        success, message = ApiKeyService.delete_api_key(api_key_id)
        
        if success:
            return ResponseUtils.success_response(message=message)
        else:
            status_code = 404 if 'não encontrada' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@api_key_bp.route('/api-keys/<int:api_key_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_api_key(current_user, api_key_id):
    """Desativar API Key (requer privilégios de admin)"""
    try:
        success, message = ApiKeyService.deactivate_api_key(api_key_id)
        
        if success:
            return ResponseUtils.success_response(message=message)
        else:
            status_code = 404 if 'não encontrada' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@api_key_bp.route('/api-keys/<int:api_key_id>/activate', methods=['POST'])
@admin_required
def activate_api_key(current_user, api_key_id):
    """Ativar API Key (requer privilégios de admin)"""
    try:
        success, message = ApiKeyService.activate_api_key(api_key_id)
        
        if success:
            return ResponseUtils.success_response(message=message)
        else:
            status_code = 404 if 'não encontrada' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@api_key_bp.route('/api-keys/my-keys', methods=['GET'])
@token_required
def get_my_api_keys(current_user):
    """Listar API Keys do usuário atual"""
    try:
        api_keys = ApiKeyService.get_user_api_keys(current_user.id)
        api_keys_data = [api_key.to_dict() for api_key in api_keys]
        
        return ResponseUtils.success_response(
            data={
                'api_keys': api_keys_data,
                'total': len(api_keys_data)
            },
            message='Suas API Keys listadas com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@api_key_bp.route('/api-keys/my-keys', methods=['POST'])
@token_required
def create_my_api_key(current_user):
    """Criar nova API Key para o usuário atual"""
    try:
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        # Definir o user_id como o usuário atual
        data['user_id'] = current_user.id
        
        api_key, success, message = ApiKeyService.create_api_key(data)
        
        if success:
            return ResponseUtils.success_response(
                data={
                    'api_key': api_key.to_dict(include_key=True)
                },
                message=message,
                status_code=201
            )
        else:
            return ResponseUtils.error_response(message, status_code=400)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )
