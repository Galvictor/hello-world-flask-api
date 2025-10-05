"""
Controlador de autenticação - Endpoints relacionados à autenticação
"""
from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.models.user import User
from app.utils.response_utils import ResponseUtils

# Criar blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        # Validar dados incluindo senha
        is_valid, error_message = User.validate_data(data, include_password=True)
        if not is_valid:
            return ResponseUtils.error_response(error_message, status_code=400)
        
        # Criar usuário
        user, success, message = UserService.create_user(data)
        
        if success:
            # Criar token de acesso
            access_token = AuthService.create_access_token(user.id)
            
            return ResponseUtils.success_response(
                data={
                    'user': user.to_dict(),
                    'access_token': access_token,
                    'token_type': 'bearer'
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

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Fazer login do usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return ResponseUtils.error_response(
                'Dados JSON são obrigatórios',
                status_code=400
            )
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return ResponseUtils.error_response(
                'Email e senha são obrigatórios',
                status_code=400
            )
        
        # Autenticar usuário
        user, access_token = AuthService.authenticate_user(email, password)
        
        if user and access_token:
            return ResponseUtils.success_response(
                data={
                    'user': user.to_dict(),
                    'access_token': access_token,
                    'token_type': 'bearer'
                },
                message='Login realizado com sucesso'
            )
        else:
            return ResponseUtils.error_response(
                'Email ou senha inválidos',
                status_code=401
            )
    
    except Exception as e:
        return ResponseUtils.error_response(
            f'Erro interno do servidor: {str(e)}',
            status_code=500
        )

@auth_bp.route('/auth/me', methods=['GET'])
def get_current_user():
    """Obter informações do usuário atual"""
    try:
        token = None
        
        # Verificar se o token está no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return ResponseUtils.error_response(
                    'Token mal formatado',
                    status_code=401
                )
        
        if not token:
            return ResponseUtils.error_response(
                'Token de acesso é obrigatório',
                status_code=401
            )
        
        # Obter usuário atual
        current_user = AuthService.get_current_user(token)
        
        return ResponseUtils.success_response(
            data={'user': current_user.to_dict()},
            message='Usuário obtido com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            'Token inválido ou expirado',
            status_code=401
        )

@auth_bp.route('/auth/refresh', methods=['POST'])
def refresh_token():
    """Renovar token de acesso"""
    try:
        token = None
        
        # Verificar se o token está no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return ResponseUtils.error_response(
                    'Token mal formatado',
                    status_code=401
                )
        
        if not token:
            return ResponseUtils.error_response(
                'Token de acesso é obrigatório',
                status_code=401
            )
        
        # Renovar token
        new_token = AuthService.refresh_token(token)
        
        return ResponseUtils.success_response(
            data={
                'access_token': new_token,
                'token_type': 'bearer'
            },
            message='Token renovado com sucesso'
        )
    
    except Exception as e:
        return ResponseUtils.error_response(
            'Token inválido ou expirado',
            status_code=401
        )
