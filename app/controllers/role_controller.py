"""
Controlador de Role - Endpoints relacionados aos roles
"""
from flask import Blueprint, jsonify, request
from app.services.role_service import RoleService
from app.utils.auth_decorators import admin_required, token_required
from app.utils.response_utils import ResponseUtils

# Criar blueprint
role_bp = Blueprint('roles', __name__)

@role_bp.route('/roles', methods=['GET'])
@admin_required
def get_roles(current_user):
    """Listar todos os roles (requer privilégios de admin)"""
    try:
        roles = RoleService.get_all_roles()
        roles_data = [role.to_dict() for role in roles]
        total = RoleService.get_roles_count()
        
        return ResponseUtils.success_response(
            data={
                'roles': roles_data,
                'total': total
            },
            message='Roles listados com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@role_bp.route('/roles', methods=['POST'])
@admin_required
def create_role(current_user):
    """Criar novo role (requer privilégios de admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        role, success, message = RoleService.create_role(data)
        
        if success:
            return ResponseUtils.success_response(
                data={'role': role.to_dict()},
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

@role_bp.route('/roles/<int:role_id>', methods=['GET'])
@admin_required
def get_role(current_user, role_id):
    """Buscar role por ID (requer privilégios de admin)"""
    try:
        role = RoleService.get_role_by_id(role_id)
        
        if not role:
            return ResponseUtils.error_response(
                'Role não encontrado',
                status_code=404
            )
        
        return ResponseUtils.success_response(
            data={'role': role.to_dict()},
            message='Role encontrado com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
@admin_required
def update_role(current_user, role_id):
    """Atualizar role (requer privilégios de admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        role, success, message = RoleService.update_role(role_id, data)
        
        if success:
            return ResponseUtils.success_response(
                data={'role': role.to_dict()},
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

@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@admin_required
def delete_role(current_user, role_id):
    """Deletar role (requer privilégios de admin)"""
    try:
        success, message = RoleService.delete_role(role_id)
        
        if success:
            return ResponseUtils.success_response(message=message)
        else:
            status_code = 404 if 'não encontrado' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@role_bp.route('/roles/initialize', methods=['POST'])
@admin_required
def initialize_roles(current_user):
    """Inicializar roles padrão do sistema (requer privilégios de admin)"""
    try:
        success, message = RoleService.initialize_default_roles()
        
        if success:
            return ResponseUtils.success_response(message=message)
        else:
            return ResponseUtils.error_response(message, status_code=400)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@role_bp.route('/users/<int:user_id>/roles', methods=['GET'])
@admin_required
def get_user_roles(current_user, user_id):
    """Listar roles de um usuário (requer privilégios de admin)"""
    try:
        roles = RoleService.get_user_roles(user_id)
        roles_data = [role.to_dict() for role in roles]
        
        return ResponseUtils.success_response(
            data={
                'user_id': user_id,
                'roles': roles_data,
                'total': len(roles_data)
            },
            message='Roles do usuário listados com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@role_bp.route('/users/<int:user_id>/roles/<int:role_id>', methods=['POST'])
@admin_required
def assign_role_to_user(current_user, user_id, role_id):
    """Atribuir role a um usuário (requer privilégios de admin)"""
    try:
        success, message = RoleService.assign_role_to_user(
            user_id, role_id, current_user.id
        )
        
        if success:
            return ResponseUtils.success_response(message=message)
        else:
            status_code = 404 if 'não encontrado' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@role_bp.route('/users/<int:user_id>/roles/<int:role_id>', methods=['DELETE'])
@admin_required
def remove_role_from_user(current_user, user_id, role_id):
    """Remover role de um usuário (requer privilégios de admin)"""
    try:
        success, message = RoleService.remove_role_from_user(user_id, role_id)
        
        if success:
            return ResponseUtils.success_response(message=message)
        else:
            status_code = 404 if 'não encontrado' in message.lower() else 400
            return ResponseUtils.error_response(message, status_code=status_code)
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@role_bp.route('/roles/<int:role_id>/users', methods=['GET'])
@admin_required
def get_role_users(current_user, role_id):
    """Listar usuários de um role (requer privilégios de admin)"""
    try:
        users = RoleService.get_role_users(role_id)
        users_data = [user.to_dict(include_roles=False) for user in users]
        
        return ResponseUtils.success_response(
            data={
                'role_id': role_id,
                'users': users_data,
                'total': len(users_data)
            },
            message='Usuários do role listados com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@role_bp.route('/users/my-roles', methods=['GET'])
@token_required
def get_my_roles(current_user):
    """Listar roles do usuário atual"""
    try:
        roles = RoleService.get_user_roles(current_user.id)
        roles_data = [role.to_dict() for role in roles]
        
        return ResponseUtils.success_response(
            data={
                'roles': roles_data,
                'total': len(roles_data),
                'permissions': current_user.get_all_permissions()
            },
            message='Seus roles listados com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )
