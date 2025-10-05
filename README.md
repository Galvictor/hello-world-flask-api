# Hello World Flask API

Uma API simples em Flask com SQLite para demonstrar funcionalidades básicas de uma API REST, operações CRUD e autenticação JWT.

## 🚀 Funcionalidades

-   **Endpoint principal** (`/`): Retorna uma mensagem de Hello World
-   **Health Check** (`/health`): Verifica se a API está funcionando
-   **Informações da API** (`/info`): Retorna detalhes sobre a API e seus endpoints
-   **CRUD de Usuários**: Operações completas de Create, Read, Update e Delete para usuários
-   **Autenticação JWT**: Sistema completo de autenticação com tokens JWT
-   **API Keys**: Sistema de chaves de API para autenticação de serviços
-   **Sistema de Roles**: Controle de acesso baseado em papéis (admin, client)
-   **Permissões Granulares**: Sistema de permissões específicas por role
-   **Rotas Protegidas**: Middleware para proteger endpoints que requerem autenticação
-   **Múltiplos Tipos de Auth**: Suporte a JWT, API Key ou ambos
-   **Banco de dados Flexível**: Suporte a SQLite, PostgreSQL e MySQL via configuração
-   **Configuração via .env**: Variáveis de ambiente para configuração segura
-   **Arquitetura em Camadas**: Código organizado seguindo padrões profissionais

## 📋 Pré-requisitos

-   Python 3.7 ou superior
-   pip (gerenciador de pacotes do Python)

## 🛠️ Instalação e Configuração

### 1. Clone ou baixe o projeto

### 2. Navegue até o diretório do projeto

```bash
cd hello-world-flask-api
```

### 3. Ative o ambiente virtual

```bash
# No Windows
.venv\Scripts\activate

# No Linux/Mac
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Como Executar

### 1. Certifique-se de que o ambiente virtual está ativo

```bash
# No Windows
.venv\Scripts\activate

# No Linux/Mac
source .venv/bin/activate
```

### 2. Execute a aplicação

```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

## 📡 Endpoints Disponíveis

### GET `/`

Retorna uma mensagem de boas-vindas.

**Resposta:**

```json
{
    "message": "Hello, World!",
    "status": "success",
    "api": "Flask API com SQLite"
}
```

### GET `/health`

Verifica se a API está funcionando corretamente.

**Resposta:**

```json
{
    "status": "healthy",
    "message": "API está funcionando corretamente",
    "database": "SQLite conectado"
}
```

### GET `/info`

Retorna informações sobre a API e seus endpoints.

**Resposta:**

```json
{
    "name": "Hello World Flask API",
    "version": "1.0.0",
    "description": "Uma API simples em Flask com SQLite para demonstrar funcionalidades básicas",
    "database": "SQLite",
    "endpoints": [
        {
            "path": "/",
            "method": "GET",
            "description": "Mensagem de boas-vindas"
        },
        {
            "path": "/health",
            "method": "GET",
            "description": "Verificação de saúde da API"
        },
        {
            "path": "/info",
            "method": "GET",
            "description": "Informações sobre a API"
        },
        {
            "path": "/users",
            "method": "GET",
            "description": "Listar todos os usuários"
        },
        {
            "path": "/users",
            "method": "POST",
            "description": "Criar novo usuário"
        },
        {
            "path": "/users/<id>",
            "method": "GET",
            "description": "Buscar usuário por ID"
        },
        {
            "path": "/users/<id>",
            "method": "PUT",
            "description": "Atualizar usuário"
        },
        {
            "path": "/users/<id>",
            "method": "DELETE",
            "description": "Deletar usuário"
        }
    ]
}
```

## 🔐 Autenticação

### POST `/api/auth/register`

Registra um novo usuário no sistema.

**Corpo da requisição:**

```json
{
    "name": "João Silva",
    "email": "joao@email.com",
    "password": "123456"
}
```

**Resposta:**

```json
{
    "data": {
        "user": {
            "id": 1,
            "name": "João Silva",
            "email": "joao@email.com",
            "is_active": true,
            "created_at": "2025-10-04T23:53:51.840154",
            "updated_at": "2025-10-04T23:53:51.840157"
        },
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    },
    "message": "Usuário criado com sucesso",
    "status": "success",
    "status_code": 201
}
```

### POST `/api/auth/login`

Faz login do usuário e retorna um token JWT.

**Corpo da requisição:**

```json
{
    "email": "joao@email.com",
    "password": "123456"
}
```

**Resposta:**

```json
{
    "data": {
        "user": {
            "id": 1,
            "name": "João Silva",
            "email": "joao@email.com",
            "is_active": true,
            "created_at": "2025-10-04T23:53:51.840154",
            "updated_at": "2025-10-04T23:53:51.840157"
        },
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    },
    "message": "Login realizado com sucesso",
    "status": "success",
    "status_code": 200
}
```

### GET `/api/auth/me`

Obtém informações do usuário atual (requer token).

**Headers:**

```
Authorization: Bearer <token>
```

### POST `/api/auth/refresh`

Renova o token de acesso (requer token válido).

**Headers:**

```
Authorization: Bearer <token>
```

## 🔑 API Keys

### POST `/api/api-keys/my-keys`

Cria uma nova API Key para o usuário atual (requer JWT token).

**Headers:**

```
Authorization: Bearer <token>
```

**Corpo da requisição:**

```json
{
    "name": "Minha API Key",
    "description": "API Key para integração com meu sistema"
}
```

**Resposta:**

```json
{
    "data": {
        "api_key": {
            "id": 1,
            "name": "Minha API Key",
            "description": "API Key para integração com meu sistema",
            "key": "4KEYgxqqg57fC_hkTZolcCsm5p7K2J3BTTFB0oyq5JU",
            "is_active": true,
            "user_id": 1,
            "created_at": "2025-10-05T00:02:08.466136",
            "expires_at": null,
            "last_used_at": null,
            "is_expired": false
        }
    },
    "message": "API Key criada com sucesso",
    "status": "success",
    "status_code": 201
}
```

### GET `/api/api-keys/my-keys`

Lista todas as API Keys do usuário atual (requer JWT token).

**Headers:**

```
Authorization: Bearer <token>
```

### Usando API Keys para Autenticação

As API Keys podem ser usadas de duas formas:

#### 1. Header X-API-Key

```bash
curl http://localhost:5000/api/users \
  -H "X-API-Key: 4KEYgxqqg57fC_hkTZolcCsm5p7K2J3BTTFB0oyq5JU"
```

#### 2. Header Authorization

```bash
curl http://localhost:5000/api/users \
  -H "Authorization: ApiKey 4KEYgxqqg57fC_hkTZolcCsm5p7K2J3BTTFB0oyq5JU"
```

### Gerenciamento de API Keys (Admin)

-   `GET /api/api-keys` - Listar todas as API Keys (admin)
-   `POST /api/api-keys` - Criar nova API Key (admin)
-   `GET /api/api-keys/<id>` - Buscar API Key por ID (admin)
-   `PUT /api/api-keys/<id>` - Atualizar API Key (admin)
-   `DELETE /api/api-keys/<id>` - Deletar API Key (admin)
-   `POST /api/api-keys/<id>/activate` - Ativar API Key (admin)
-   `POST /api/api-keys/<id>/deactivate` - Desativar API Key (admin)

## 👑 Sistema de Roles

### GET `/api/roles`

Lista todos os roles do sistema (requer role admin).

**Headers:**

```
Authorization: Bearer <token>
```

### GET `/api/users/my-roles`

Lista os roles do usuário atual.

**Headers:**

```
Authorization: Bearer <token>
```

**Resposta:**

```json
{
    "data": {
        "roles": [
            {
                "id": 2,
                "name": "client",
                "display_name": "Cliente",
                "description": "Usuário padrão do sistema",
                "permissions": ["users:read_own", "users:write_own"],
                "is_active": true
            }
        ],
        "permissions": ["users:read_own", "users:write_own", "api_keys:read_own", "api_keys:write_own", "api_keys:delete_own"],
        "total": 1
    },
    "message": "Seus roles listados com sucesso",
    "status": "success"
}
```

### Roles Padrão

#### Admin

-   **Permissões**: Acesso total ao sistema
-   **Inclui**: `users:read`, `users:write`, `users:delete`, `api_keys:read`, `api_keys:write`, `api_keys:delete`, `roles:read`, `roles:write`, `roles:delete`, `system:admin`

#### Client

-   **Permissões**: Acesso limitado aos próprios recursos
-   **Inclui**: `users:read_own`, `users:write_own`, `api_keys:read_own`, `api_keys:write_own`, `api_keys:delete_own`

### Gerenciamento de Roles (Admin)

-   `GET /api/roles` - Listar todos os roles (admin)
-   `POST /api/roles` - Criar novo role (admin)
-   `GET /api/roles/<id>` - Buscar role por ID (admin)
-   `PUT /api/roles/<id>` - Atualizar role (admin)
-   `DELETE /api/roles/<id>` - Deletar role (admin)
-   `GET /api/users/<id>/roles` - Listar roles de um usuário (admin)
-   `POST /api/users/<id>/roles/<role_id>` - Atribuir role a usuário (admin)
-   `DELETE /api/users/<id>/roles/<role_id>` - Remover role de usuário (admin)
-   `GET /api/roles/<id>/users` - Listar usuários de um role (admin)

### Decoradores de Autenticação

#### `@admin_required`

Protege rotas que requerem role de administrador.

#### `@role_required('role_name')`

Protege rotas que requerem um role específico.

#### `@permission_required('permission')`

Protege rotas que requerem uma permissão específica.

## 👥 Endpoints de Usuários

### GET `/api/users`

Lista todos os usuários cadastrados (requer JWT token ou API Key).

**Headers (JWT):**

```
Authorization: Bearer <token>
```

**Headers (API Key):**

```
X-API-Key: <api_key>
```

ou

```
Authorization: ApiKey <api_key>
```

**Resposta:**

```json
{
    "users": [
        {
            "id": 1,
            "name": "João Silva",
            "email": "joao@email.com",
            "created_at": "2025-10-04T23:01:16.049502"
        }
    ],
    "total": 1
}
```

### POST `/users`

Cria um novo usuário.

**Corpo da requisição:**

```json
{
    "name": "João Silva",
    "email": "joao@email.com"
}
```

**Resposta:**

```json
{
    "message": "Usuário criado com sucesso",
    "user": {
        "id": 1,
        "name": "João Silva",
        "email": "joao@email.com",
        "created_at": "2025-10-04T23:01:16.049502"
    },
    "status": "success"
}
```

### GET `/users/<id>`

Busca um usuário específico por ID.

**Resposta:**

```json
{
    "user": {
        "id": 1,
        "name": "João Silva",
        "email": "joao@email.com",
        "created_at": "2025-10-04T23:01:16.049502"
    },
    "status": "success"
}
```

### PUT `/users/<id>`

Atualiza um usuário existente.

**Corpo da requisição:**

```json
{
    "name": "João Silva Atualizado",
    "email": "joao.novo@email.com"
}
```

**Resposta:**

```json
{
    "message": "Usuário atualizado com sucesso",
    "user": {
        "id": 1,
        "name": "João Silva Atualizado",
        "email": "joao.novo@email.com",
        "created_at": "2025-10-04T23:01:16.049502"
    },
    "status": "success"
}
```

### DELETE `/users/<id>`

Remove um usuário do sistema.

**Resposta:**

```json
{
    "message": "Usuário deletado com sucesso",
    "status": "success"
}
```

## 🧪 Testando a API

### Usando cURL

```bash
# Testar endpoint principal
curl http://localhost:5000/

# Testar health check
curl http://localhost:5000/health

# Testar informações da API
curl http://localhost:5000/info

# Listar usuários
curl http://localhost:5000/users

# Criar usuário
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"João Silva","email":"joao@email.com"}'

# Buscar usuário por ID
curl http://localhost:5000/users/1

# Atualizar usuário
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"João Silva Atualizado","email":"joao.novo@email.com"}'

# Deletar usuário
curl -X DELETE http://localhost:5000/users/1
```

### Usando PowerShell (Windows)

```powershell
# Criar usuário
$body = '{"name":"João Silva","email":"joao@email.com"}'
Invoke-RestMethod -Uri "http://localhost:5000/users" -Method POST -Body $body -ContentType "application/json"

# Atualizar usuário
$body = '{"name":"João Silva Atualizado","email":"joao.novo@email.com"}'
Invoke-RestMethod -Uri "http://localhost:5000/users/1" -Method PUT -Body $body -ContentType "application/json"
```

### Usando Python requests

```python
import requests

# Testar endpoint principal
response = requests.get('http://localhost:5000/')
print(response.json())

# Criar usuário
user_data = {"name": "João Silva", "email": "joao@email.com"}
response = requests.post('http://localhost:5000/users', json=user_data)
print(response.json())

# Listar usuários
response = requests.get('http://localhost:5000/users')
print(response.json())

# Buscar usuário por ID
response = requests.get('http://localhost:5000/users/1')
print(response.json())

# Atualizar usuário
update_data = {"name": "João Silva Atualizado", "email": "joao.novo@email.com"}
response = requests.put('http://localhost:5000/users/1', json=update_data)
print(response.json())

# Deletar usuário
response = requests.delete('http://localhost:5000/users/1')
print(response.json())
```

## 🔧 Desenvolvimento

Para desenvolvimento, a aplicação está configurada com:

-   **Debug mode**: Ativado (para recarregamento automático)
-   **Host**: 0.0.0.0 (aceita conexões de qualquer IP)
-   **Porta**: 5000
-   **Banco de dados**: SQLite (arquivo `database.db` criado automaticamente)

## 📦 Estrutura do Projeto

```
hello-world-flask-api/
├── .venv/                 # Ambiente virtual Python
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências do projeto
├── database.db           # Banco de dados SQLite (criado automaticamente)
└── README.md             # Este arquivo
```

## 🗄️ Modelo de Dados

### User

-   `id` (Integer, Primary Key): ID único do usuário
-   `name` (String, 100 chars): Nome do usuário
-   `email` (String, 120 chars, Unique): Email do usuário
-   `created_at` (DateTime): Data de criação do usuário

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
