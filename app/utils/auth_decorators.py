"""
Decoradores de autenticação para proteger rotas
"""
from functools import wraps
from flask import request, jsonify
from jose import JWTError
from app.services.auth_service import AuthService
from app.services.api_key_service import ApiKeyService

def token_required(f):
    """
    Decorador para proteger rotas que requerem autenticação
    
    Adiciona o usuário autenticado ao contexto da função como 'current_user'
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Verificar se o token está no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Formato: "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({
                    'error': 'Token mal formatado',
                    'status': 'error'
                }), 401
        
        if not token:
            return jsonify({
                'error': 'Token de acesso é obrigatório',
                'status': 'error'
            }), 401
        
        try:
            # Verificar e obter usuário do token
            current_user = AuthService.get_current_user(token)
            
            # Adicionar usuário ao contexto da função
            return f(current_user, *args, **kwargs)
            
        except JWTError as e:
            return jsonify({
                'error': 'Token inválido ou expirado',
                'status': 'error'
            }), 401
        except Exception as e:
            return jsonify({
                'error': f'Erro de autenticação: {str(e)}',
                'status': 'error'
            }), 500
    
    return decorated

def api_key_required(f):
    """
    Decorador para proteger rotas que requerem API Key
    
    Adiciona a API Key validada ao contexto da função como 'current_api_key'
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = None
        
        # Verificar se a API Key está no header X-API-Key ou Authorization
        if 'X-API-Key' in request.headers:
            api_key = request.headers['X-API-Key']
        elif 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Formato: "ApiKey <key>"
                if auth_header.startswith('ApiKey '):
                    api_key = auth_header.split(" ")[1]
            except IndexError:
                pass
        
        if not api_key:
            return jsonify({
                'error': 'API Key é obrigatória',
                'status': 'error'
            }), 401
        
        try:
            # Validar API Key
            api_key_obj, is_valid, message = ApiKeyService.validate_api_key(api_key)
            
            if not is_valid:
                return jsonify({
                    'error': message,
                    'status': 'error'
                }), 401
            
            # Adicionar API Key ao contexto da função
            return f(api_key_obj, *args, **kwargs)
            
        except Exception as e:
            return jsonify({
                'error': f'Erro de validação da API Key: {str(e)}',
                'status': 'error'
            }), 500
    
    return decorated

def admin_required(f):
    """
    Decorador para proteger rotas que requerem privilégios de administrador
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Aplicar autenticação primeiro
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]
            except IndexError:
                pass
        
        if not token:
            return jsonify({
                'error': 'Token de acesso é obrigatório',
                'status': 'error'
            }), 401
        
        try:
            # Verificar token e obter usuário
            current_user = AuthService.get_current_user(token)
            
            # Verificar se o usuário tem role de admin
            if not current_user or not current_user.has_role('admin'):
                return jsonify({
                    'error': 'Acesso negado. Privilégios de administrador são necessários.',
                    'status': 'error'
                }), 403
            
            # Executar função com o usuário autenticado
            return f(current_user, *args, **kwargs)
            
        except JWTError:
            return jsonify({
                'error': 'Token inválido ou expirado',
                'status': 'error'
            }), 401
        except Exception as e:
            return jsonify({
                'error': f'Erro de autenticação: {str(e)}',
                'status': 'error'
            }), 500
    
    return decorated

def permission_required(permission):
    """
    Decorador para proteger rotas que requerem uma permissão específica
    
    Args:
        permission (str): Permissão necessária (ex: 'users:read', 'api_keys:write')
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Primeiro aplicar autenticação
            auth_result = token_required(f)(*args, **kwargs)
            
            # Se retornou uma resposta de erro (não é uma função), retornar
            if not callable(auth_result):
                return auth_result
            
            # Verificar se o usuário tem a permissão necessária
            current_user = args[0] if args else None
            
            if not current_user or not current_user.has_permission(permission):
                return jsonify({
                    'error': f'Acesso negado. Permissão "{permission}" é necessária.',
                    'status': 'error'
                }), 403
            
            return auth_result
        
        return decorated
    return decorator

def role_required(role_name):
    """
    Decorador para proteger rotas que requerem um role específico
    
    Args:
        role_name (str): Nome do role necessário (ex: 'admin', 'client')
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Primeiro aplicar autenticação
            auth_result = token_required(f)(*args, **kwargs)
            
            # Se retornou uma resposta de erro (não é uma função), retornar
            if not callable(auth_result):
                return auth_result
            
            # Verificar se o usuário tem o role necessário
            current_user = args[0] if args else None
            
            if not current_user or not current_user.has_role(role_name):
                return jsonify({
                    'error': f'Acesso negado. Role "{role_name}" é necessário.',
                    'status': 'error'
                }), 403
            
            return auth_result
        
        return decorated
    return decorator

def auth_or_api_key_required(f):
    """
    Decorador que aceita tanto JWT token quanto API Key
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = None
        current_api_key = None
        
        # Verificar se há token JWT
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                try:
                    token = auth_header.split(" ")[1]
                    current_user = AuthService.get_current_user(token)
                    
                    # SEGURANÇA: Verificar se usuário tem pelo menos um role
                    if current_user and not current_user.roles:
                        return jsonify({
                            'error': 'Usuário não possui roles atribuídos. Acesso negado.',
                            'status': 'error'
                        }), 403
                    
                    return f(current_user=current_user, current_api_key=None, *args, **kwargs)
                except JWTError:
                    pass
        
        # Se não há token JWT válido, verificar API Key
        api_key = None
        if 'X-API-Key' in request.headers:
            api_key = request.headers['X-API-Key']
        elif 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                if auth_header.startswith('ApiKey '):
                    api_key = auth_header.split(" ")[1]
            except IndexError:
                pass
        
        if api_key:
            try:
                api_key_obj, is_valid, message = ApiKeyService.validate_api_key(api_key)
                if is_valid:
                    return f(current_user=None, current_api_key=api_key_obj, *args, **kwargs)
            except Exception:
                pass
        
        return jsonify({
            'error': 'Token JWT ou API Key é obrigatório',
            'status': 'error'
        }), 401
    
    return decorated
