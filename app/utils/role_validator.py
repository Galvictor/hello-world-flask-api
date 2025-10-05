"""
Utilitário para validação e consistência de roles
"""
from app.models.user import User
from app.models.role import Role
from app.services.role_service import RoleService
from app import db

class RoleValidator:
    """Classe para validações de consistência do sistema de roles"""
    
    @staticmethod
    def validate_user_roles(user_id: int) -> tuple[bool, str, list]:
        """
        Valida se um usuário tem roles consistentes
        
        Returns:
            Tuple[bool, str, list]: (is_valid, message, issues)
        """
        issues = []
        
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "Usuário não encontrado", ["Usuário não existe"]
            
            # Verificar se usuário tem pelo menos um role
            if not user.roles:
                issues.append("Usuário não possui nenhum role")
            
            # Verificar se todos os roles estão ativos
            inactive_roles = [role.name for role in user.roles if not role.is_active]
            if inactive_roles:
                issues.append(f"Usuário possui roles inativos: {', '.join(inactive_roles)}")
            
            # Verificar se roles existem e estão válidos
            for role in user.roles:
                if not role.is_active:
                    issues.append(f"Role '{role.name}' está inativo")
                
                if not role.permissions:
                    issues.append(f"Role '{role.name}' não possui permissões")
            
            is_valid = len(issues) == 0
            message = "Usuário válido" if is_valid else "Usuário possui inconsistências"
            
            return is_valid, message, issues
            
        except Exception as e:
            return False, f"Erro na validação: {str(e)}", [str(e)]
    
    @staticmethod
    def validate_all_users() -> dict:
        """
        Valida todos os usuários do sistema
        
        Returns:
            dict: Relatório de validação
        """
        report = {
            'total_users': 0,
            'valid_users': 0,
            'invalid_users': 0,
            'users_without_roles': 0,
            'issues': []
        }
        
        try:
            users = User.query.all()
            report['total_users'] = len(users)
            
            for user in users:
                is_valid, message, issues = RoleValidator.validate_user_roles(user.id)
                
                if not user.roles:
                    report['users_without_roles'] += 1
                
                if is_valid:
                    report['valid_users'] += 1
                else:
                    report['invalid_users'] += 1
                    report['issues'].append({
                        'user_id': user.id,
                        'user_email': user.email,
                        'issues': issues
                    })
            
            return report
            
        except Exception as e:
            report['issues'].append(f"Erro geral: {str(e)}")
            return report
    
    @staticmethod
    def fix_user_without_roles(user_id: int) -> tuple[bool, str]:
        """
        Corrige usuário sem roles atribuindo role 'client' por padrão
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "Usuário não encontrado"
            
            if user.roles:
                return False, "Usuário já possui roles"
            
            # Atribuir role 'client' por padrão
            client_role = RoleService.get_role_by_name('client')
            if not client_role:
                return False, "Role 'client' não encontrado"
            
            user.add_role(client_role)
            return True, f"Role 'client' atribuído ao usuário {user.email}"
            
        except Exception as e:
            return False, f"Erro ao corrigir usuário: {str(e)}"
    
    @staticmethod
    def fix_all_users_without_roles() -> dict:
        """
        Corrige todos os usuários sem roles
        
        Returns:
            dict: Relatório de correções
        """
        report = {
            'total_fixed': 0,
            'total_errors': 0,
            'fixed_users': [],
            'errors': []
        }
        
        try:
            users = User.query.all()
            
            for user in users:
                if not user.roles:
                    success, message = RoleValidator.fix_user_without_roles(user.id)
                    
                    if success:
                        report['total_fixed'] += 1
                        report['fixed_users'].append({
                            'user_id': user.id,
                            'user_email': user.email,
                            'message': message
                        })
                    else:
                        report['total_errors'] += 1
                        report['errors'].append({
                            'user_id': user.id,
                            'user_email': user.email,
                            'error': message
                        })
            
            return report
            
        except Exception as e:
            report['errors'].append(f"Erro geral: {str(e)}")
            return report
    
    @staticmethod
    def validate_role_permissions() -> dict:
        """
        Valida se todos os roles têm permissões válidas
        
        Returns:
            dict: Relatório de validação
        """
        report = {
            'total_roles': 0,
            'valid_roles': 0,
            'invalid_roles': 0,
            'issues': []
        }
        
        try:
            roles = Role.query.filter_by(is_active=True).all()
            report['total_roles'] = len(roles)
            
            for role in roles:
                issues = []
                
                # Verificar se role tem permissões
                if not role.permissions:
                    issues.append("Role não possui permissões")
                
                # Verificar se permissões são uma lista válida
                if role.permissions and not isinstance(role.permissions, list):
                    issues.append("Permissões devem ser uma lista")
                
                if issues:
                    report['invalid_roles'] += 1
                    report['issues'].append({
                        'role_id': role.id,
                        'role_name': role.name,
                        'issues': issues
                    })
                else:
                    report['valid_roles'] += 1
            
            return report
            
        except Exception as e:
            report['issues'].append(f"Erro geral: {str(e)}")
            return report
    
    @staticmethod
    def get_system_health_report() -> dict:
        """
        Gera relatório completo de saúde do sistema de roles
        
        Returns:
            dict: Relatório completo
        """
        user_report = RoleValidator.validate_all_users()
        role_report = RoleValidator.validate_role_permissions()
        
        from datetime import datetime
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'users': user_report,
            'roles': role_report,
            'overall_health': 'healthy' if (
                user_report['invalid_users'] == 0 and 
                role_report['invalid_roles'] == 0
            ) else 'issues_found'
        }
