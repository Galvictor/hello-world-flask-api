"""
Utilitário para inicializar dados padrão do sistema
"""
from app.services.role_service import RoleService
from app.services.user_service import UserService
from app.models.user import User
from app import db

def initialize_default_data():
    """
    Inicializa os dados padrão do sistema:
    - Roles padrão (admin, client)
    - Usuário administrador padrão (se não existir)
    """
    try:
        # Inicializar roles padrão
        roles_success, roles_message = RoleService.initialize_default_roles()
        if not roles_success:
            print(f"Erro ao inicializar roles: {roles_message}")
            return False, roles_message
        
        print("Roles padrao inicializados com sucesso")
        
        # Verificar se já existe um usuário admin
        admin_user = User.query.filter_by(email='admin@system.com').first()
        
        if not admin_user:
            # Criar usuário administrador padrão
            admin_data = {
                'name': 'Administrador do Sistema',
                'email': 'admin@system.com',
                'password': 'admin123'
            }
            
            admin_user, success, message = UserService.create_user(admin_data)
            
            if success:
                # Atribuir role de admin
                admin_role = RoleService.get_role_by_name('admin')
                if admin_role:
                    admin_user.add_role(admin_role)
                    print("Usuario administrador criado com sucesso")
                else:
                    print("Usuario criado, mas role admin nao encontrado")
            else:
                print(f"Erro ao criar usuario admin: {message}")
                return False, message
        else:
            print("Usuario administrador ja existe")
        
        return True, "Dados padrão inicializados com sucesso"
    
    except Exception as e:
        print(f"Erro ao inicializar dados padrao: {str(e)}")
        return False, f"Erro ao inicializar dados padrão: {str(e)}"

def create_test_client():
    """
    Cria um usuário cliente de teste
    """
    try:
        # Verificar se já existe
        client_user = User.query.filter_by(email='client@test.com').first()
        
        if not client_user:
            client_data = {
                'name': 'Cliente de Teste',
                'email': 'client@test.com',
                'password': 'client123'
            }
            
            client_user, success, message = UserService.create_user(client_data)
            
            if success:
                # Atribuir role de client
                client_role = RoleService.get_role_by_name('client')
                if client_role:
                    client_user.add_role(client_role)
                    print("Usuario cliente de teste criado com sucesso")
                    return True, "Cliente de teste criado"
                else:
                    print("Usuario criado, mas role client nao encontrado")
                    return False, "Role client não encontrado"
            else:
                print(f"Erro ao criar usuario cliente: {message}")
                return False, message
        else:
            print("Usuario cliente ja existe")
            return True, "Cliente já existe"
    
    except Exception as e:
        print(f"Erro ao criar cliente de teste: {str(e)}")
        return False, f"Erro ao criar cliente de teste: {str(e)}"

def reset_and_initialize():
    """
    Reseta e inicializa todos os dados padrão
    """
    try:
        print("Inicializando dados padrao do sistema...")
        
        # Inicializar dados padrão
        success, message = initialize_default_data()
        if not success:
            return False, message
        
        # Criar cliente de teste
        client_success, client_message = create_test_client()
        
        print("Inicializacao concluida com sucesso!")
        print("\nCredenciais padrao:")
        print("Admin: admin@system.com / admin123")
        print("Cliente: client@test.com / client123")
        
        return True, "Sistema inicializado com sucesso"
    
    except Exception as e:
        print(f"Erro na inicializacao: {str(e)}")
        return False, f"Erro na inicialização: {str(e)}"
