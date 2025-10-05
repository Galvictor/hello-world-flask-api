"""
Controlador de usuário - Endpoints relacionados aos usuários
"""
from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
from app.utils.auth_decorators import token_required, admin_required, auth_or_api_key_required
from app.utils.response_utils import ResponseUtils

# Criar blueprint
user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
@auth_or_api_key_required
def get_users(current_user=None, current_api_key=None):
    """
    Listar todos os usuários
    ---
    tags:
      - Users
    summary: Obter lista de usuários
    description: Retorna todos os usuários do sistema (requer JWT token ou API Key)
    security:
      - Bearer: []
      - ApiKey: []
    responses:
      200:
        description: Lista de usuários obtida com sucesso
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            message:
              type: string
              example: Usuários listados com sucesso
            data:
              type: object
              properties:
                users:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: João Silva
                      email:
                        type: string
                        example: joao@email.com
                      is_active:
                        type: boolean
                        example: true
                      created_at:
                        type: string
                        format: date-time
                total:
                  type: integer
                  example: 5
      401:
        description: Token JWT ou API Key obrigatório
      403:
        description: Usuário sem roles atribuídos
    """
    try:
        users = UserService.get_all_users()
        users_data = [user.to_dict() for user in users]
        total = UserService.get_users_count()
        
        return ResponseUtils.success_response(
            data={
                'users': users_data,
                'total': total
            },
            message='Usuários listados com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@user_bp.route('/users', methods=['POST'])
@admin_required
def create_user(current_user):
    """Criar novo usuário (requer privilégios de admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        user, success, message = UserService.create_user(data)
        
        if success:
            return ResponseUtils.success_response(
                data={'user': user.to_dict()},
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

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """Buscar usuário por ID (requer autenticação)"""
    try:
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            return ResponseUtils.error_response(
                'Usuário não encontrado',
                status_code=404
            )
        
        return ResponseUtils.success_response(
            data={'user': user.to_dict()},
            message='Usuário encontrado com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """Atualizar usuário (requer autenticação)"""
    try:
        # Verificar se o usuário pode atualizar (próprio usuário ou admin)
        if current_user.id != user_id:
            return ResponseUtils.error_response(
                'Você só pode atualizar seus próprios dados',
                status_code=403
            )
        
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        user, success, message = UserService.update_user(user_id, data)
        
        if success:
            return ResponseUtils.success_response(
                data={'user': user.to_dict()},
                message=message
            )
        else:
            status_code = 404 if 'não encontrado' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, user_id):
    """Deletar usuário (requer privilégios de admin)"""
    try:
        success, message = UserService.delete_user(user_id)
        
        if success:
            return ResponseUtils.success_response(
                message=message
            )
        else:
            status_code = 404 if 'não encontrado' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )
