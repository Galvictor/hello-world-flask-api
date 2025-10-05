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
    
    Nota: Por enquanto, todos os usuários ativos são considerados administradores.
    Em uma implementação mais robusta, você adicionaria um campo 'role' ao modelo User.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Primeiro aplicar autenticação
        auth_result = token_required(f)(*args, **kwargs)
        
        # Se retornou uma resposta de erro (não é uma função), retornar
        if not callable(auth_result):
            return auth_result
        
        # Por enquanto, qualquer usuário autenticado é considerado admin
        # Em uma implementação futura, você verificaria o role do usuário
        return auth_result
    
    return decorated

def auth_or_api_key_required(f):
    """
    Decorador que aceita tanto JWT token quanto API Key
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Verificar se há token JWT
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                try:
                    token = auth_header.split(" ")[1]
                    current_user = AuthService.get_current_user(token)
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
