"""
Utilitários para respostas padronizadas da API
"""
from flask import jsonify
from typing import Any, Dict, Optional

class ResponseUtils:
    """Classe utilitária para padronizar respostas da API"""
    
    @staticmethod
    def success_response(data: Any = None, message: str = None, status_code: int = 200) -> tuple:
        """
        Cria uma resposta de sucesso padronizada
        
        Args:
            data: Dados a serem retornados
            message: Mensagem de sucesso
            status_code: Código HTTP de status
            
        Returns:
            Tuple contendo resposta JSON e código de status
        """
        response = {
            'status': 'success',
            'status_code': status_code
        }
        
        if message:
            response['message'] = message
        
        if data is not None:
            response['data'] = data
        
        return jsonify(response), status_code
    
    @staticmethod
    def error_response(message: str, status_code: int = 400, details: Optional[Dict] = None) -> tuple:
        """
        Cria uma resposta de erro padronizada
        
        Args:
            message: Mensagem de erro
            status_code: Código HTTP de status
            details: Detalhes adicionais do erro
            
        Returns:
            Tuple contendo resposta JSON e código de status
        """
        response = {
            'status': 'error',
            'status_code': status_code,
            'error': message
        }
        
        if details:
            response['details'] = details
        
        return jsonify(response), status_code
    
    @staticmethod
    def validation_error_response(errors: Dict[str, str], status_code: int = 422) -> tuple:
        """
        Cria uma resposta de erro de validação padronizada
        
        Args:
            errors: Dicionário com erros de validação
            status_code: Código HTTP de status
            
        Returns:
            Tuple contendo resposta JSON e código de status
        """
        return ResponseUtils.error_response(
            message='Erro de validação',
            status_code=status_code,
            details={'validation_errors': errors}
        )
