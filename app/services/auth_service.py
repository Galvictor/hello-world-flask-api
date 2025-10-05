"""
Serviço de autenticação - Contém a lógica de autenticação JWT
"""
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config.app import AppConfig
from app.models.user import User
from app import db

class AuthService:
    """Serviço responsável pela autenticação e autorização"""
    
    @staticmethod
    def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
        """
        Cria um token JWT de acesso
        
        Args:
            user_id: ID do usuário
            expires_delta: Tempo de expiração personalizado
            
        Returns:
            Token JWT codificado
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(seconds=AppConfig.JWT_ACCESS_TOKEN_EXPIRES)
        
        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(
            to_encode, 
            AppConfig.JWT_SECRET_KEY, 
            algorithm=AppConfig.JWT_ALGORITHM
        )
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verifica e decodifica um token JWT
        
        Args:
            token: Token JWT para verificar
            
        Returns:
            Payload decodificado do token
            
        Raises:
            JWTError: Se o token for inválido
        """
        try:
            payload = jwt.decode(
                token, 
                AppConfig.JWT_SECRET_KEY, 
                algorithms=[AppConfig.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            raise JWTError("Token inválido")
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> tuple:
        """
        Autentica um usuário com email e senha
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            Tuple[User, str]: (usuário, token) se autenticado com sucesso
            Tuple[None, None]: Se autenticação falhar
        """
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return None, None
        
        if not user.is_active:
            return None, None
        
        # Criar token de acesso
        access_token = AuthService.create_access_token(user.id)
        
        return user, access_token
    
    @staticmethod
    def get_current_user(token: str) -> User:
        """
        Obtém o usuário atual baseado no token
        
        Args:
            token: Token JWT
            
        Returns:
            User: Usuário autenticado
            
        Raises:
            JWTError: Se o token for inválido
        """
        payload = AuthService.verify_token(token)
        user_id = int(payload.get("sub"))
        
        user = User.query.get(user_id)
        if not user or not user.is_active:
            raise JWTError("Usuário não encontrado ou inativo")
        
        return user
    
    @staticmethod
    def refresh_token(token: str) -> str:
        """
        Renova um token de acesso
        
        Args:
            token: Token atual
            
        Returns:
            Novo token JWT
        """
        user = AuthService.get_current_user(token)
        return AuthService.create_access_token(user.id)
