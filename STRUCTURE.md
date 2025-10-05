# Estrutura do Projeto - Arquitetura em Camadas

## 📁 Estrutura de Diretórios

```
hello-world-flask-api/
├── app/                           # Pacote principal da aplicação
│   ├── __init__.py               # Factory function e inicialização
│   ├── config/                   # Configurações da aplicação
│   │   ├── __init__.py
│   │   ├── app.py               # Configurações gerais
│   │   └── database.py          # Configurações do banco
│   ├── models/                   # Camada de modelos (Entidades)
│   │   ├── __init__.py
│   │   └── user.py              # Modelo User
│   ├── services/                 # Camada de serviços (Lógica de negócio)
│   │   ├── __init__.py
│   │   └── user_service.py      # Serviço de usuário
│   ├── controllers/              # Camada de controladores (Endpoints)
│   │   ├── __init__.py
│   │   ├── main_controller.py   # Endpoints principais
│   │   └── user_controller.py   # Endpoints de usuário
│   └── utils/                    # Utilitários e helpers
│       ├── __init__.py
│       └── response_utils.py    # Utilitários de resposta
├── .venv/                        # Ambiente virtual Python
├── app.py                       # Aplicação principal
├── requirements.txt             # Dependências
├── database.db                  # Banco SQLite (criado automaticamente)
├── README.md                    # Documentação principal
└── STRUCTURE.md                 # Este arquivo
```

## 🏗️ Arquitetura em Camadas

### 1. **Camada de Configuração** (`app/config/`)

-   **Responsabilidade**: Centralizar todas as configurações da aplicação
-   **Arquivos**:
    -   `app.py`: Configurações gerais (debug, host, port, etc.)
    -   `database.py`: Configurações do banco de dados SQLite

### 2. **Camada de Modelos** (`app/models/`)

-   **Responsabilidade**: Definir as entidades do banco de dados
-   **Arquivos**:
    -   `user.py`: Modelo User com validações e métodos auxiliares
-   **Características**:
    -   Herda de `db.Model` (SQLAlchemy)
    -   Métodos `to_dict()`, `from_dict()`, `update_from_dict()`
    -   Validações de dados

### 3. **Camada de Serviços** (`app/services/`)

-   **Responsabilidade**: Contém a lógica de negócio da aplicação
-   **Arquivos**:
    -   `user_service.py`: Operações CRUD para usuários
-   **Características**:
    -   Métodos estáticos para operações do banco
    -   Tratamento de erros e validações
    -   Retorna tuplas com (dados, sucesso, mensagem)

### 4. **Camada de Controladores** (`app/controllers/`)

-   **Responsabilidade**: Definir as rotas e endpoints da API
-   **Arquivos**:
    -   `main_controller.py`: Endpoints principais (/health, /info, etc.)
    -   `user_controller.py`: Endpoints CRUD de usuários (/api/users/\*)
-   **Características**:
    -   Usa Blueprints para organização de rotas
    -   Tratamento de requisições HTTP
    -   Chama serviços para lógica de negócio

### 5. **Camada de Utilitários** (`app/utils/`)

-   **Responsabilidade**: Funções auxiliares e helpers
-   **Arquivos**:
    -   `response_utils.py`: Padronização de respostas da API
-   **Características**:
    -   Classes utilitárias para respostas padronizadas
    -   Facilita manutenção e consistência

## 🔄 Fluxo de Dados

```
Request → Controller → Service → Model → Database
                ↓
Response ← Controller ← Service ← Model ← Database
```

### Exemplo de Fluxo:

1. **Request**: `POST /api/users` com dados JSON
2. **Controller**: `user_controller.py` recebe a requisição
3. **Service**: `user_service.py` processa a lógica de negócio
4. **Model**: `user.py` valida e cria a entidade
5. **Database**: SQLAlchemy persiste no SQLite
6. **Response**: Retorna dados padronizados

## ✅ Benefícios da Arquitetura

### 🎯 **Separação de Responsabilidades**

-   Cada camada tem uma responsabilidade específica
-   Facilita manutenção e testes
-   Reduz acoplamento entre componentes

### 🔧 **Facilidade de Manutenção**

-   Código organizado e modular
-   Fácil localização de funcionalidades
-   Reutilização de código

### 🧪 **Testabilidade**

-   Cada camada pode ser testada independentemente
-   Mocks e stubs mais fáceis de implementar
-   Testes unitários e de integração

### 📈 **Escalabilidade**

-   Fácil adição de novas funcionalidades
-   Possibilidade de trocar banco de dados
-   Adição de novas camadas (cache, autenticação, etc.)

### 🔄 **Reutilização**

-   Serviços podem ser reutilizados em diferentes controllers
-   Modelos podem ser usados em diferentes contextos
-   Utilitários compartilhados

## 🚀 Como Adicionar Novas Funcionalidades

### Para adicionar uma nova entidade (ex: Product):

1. **Modelo**: Criar `app/models/product.py`
2. **Serviço**: Criar `app/services/product_service.py`
3. **Controller**: Criar `app/controllers/product_controller.py`
4. **Registrar**: Adicionar blueprint no `app/__init__.py`

### Para adicionar novos endpoints:

1. **Controller**: Adicionar rotas no controller existente
2. **Service**: Adicionar métodos no service correspondente
3. **Model**: Adicionar métodos auxiliares se necessário

## 📝 Convenções de Código

-   **Nomes de arquivos**: snake_case
-   **Nomes de classes**: PascalCase
-   **Nomes de métodos**: snake_case
-   **Blueprints**: Nome descritivo + `_bp`
-   **Imports**: Organizados por camada
-   **Documentação**: Docstrings em todos os métodos públicos
