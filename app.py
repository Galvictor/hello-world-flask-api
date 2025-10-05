"""
Aplicação principal Flask Hello World API
Arquitetura em camadas para melhor organização e manutenibilidade
"""

from app import create_app

# Criar instância da aplicação
app = create_app()

if __name__ == '__main__':
    # Configurações de desenvolvimento
    app.run(
        debug=app.config.get('DEBUG', True),
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000)
    )