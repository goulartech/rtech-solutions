# Sistema de Gerenciamento de Solicitações

## Descrição

Aplicação completa de gerenciamento de solicitações desenvolvida em Python, oferecendo duas interfaces:
- **API REST** com FastAPI (documentação automática com Swagger)
- **Interface Web** com Streamlit (UI intuitiva e responsiva)

Sistema profissional implementando **Clean Architecture** com separação de camadas, validações robustas e testes automatizados.

## Funcionalidades

### CRUD Completo
- **Criar** novas solicitações com validações
- **Listar** todas as solicitações (com filtros por status)
- **Atualizar** solicitações existentes (completa ou parcial)
- **Excluir** solicitações por ID
- **Dashboard** com estatísticas em tempo real

### Campos da Solicitação
- **ID**: Gerado automaticamente (auto-incremento)
- **Tipo**: manutencao, suporte, desenvolvimento, consulta, outros
- **Descrição**: Texto descritivo (10-500 caracteres)
- **Status**: pendente, em_andamento, concluida, cancelada
- **Data de Criação**: Timestamp automático
- **Data de Atualização**: Atualizado automaticamente

## Arquitetura

```
desafio-dois/
├── src/
│   ├── __init__.py          # Inicialização do pacote
│   ├── models.py            # Modelos Pydantic com validações
│   ├── repository.py        # Camada de persistência (Repository Pattern)
│   ├── services.py          # Lógica de negócio
│   └── routes.py            # (Integrado em app.py)
├── data/
│   └── solicitacoes.json    # Armazenamento persistente
├── app.py                   # API REST com FastAPI
├── streamlit_app.py         # Interface Web com Streamlit
├── test_api.py              # Testes unitários e de integração
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

### Padrões e Boas Práticas

- **Clean Architecture**: Separação clara de responsabilidades
- **Repository Pattern**: Abstração da camada de dados
- **Service Layer**: Lógica de negócio centralizada
- **Dependency Injection**: Facilitando testes e manutenção
- **Type Hints**: Tipagem completa em Python
- **Validation**: Pydantic para validação de dados
- **Thread-Safe**: Operações seguras com Lock
- **REST API**: Endpoints seguindo convenções RESTful
- **OpenAPI**: Documentação automática da API

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone ou navegue até o diretório do projeto**
```bash
cd desafio-dois
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## Como Usar

### Opção 1: API REST (FastAPI)

1. **Inicie o servidor API**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

2. **Acesse a documentação interativa**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

3. **Endpoints disponíveis**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Status da aplicação |
| POST | `/solicitacoes` | Criar solicitação |
| GET | `/solicitacoes` | Listar todas |
| GET | `/solicitacoes/{id}` | Buscar por ID |
| PUT | `/solicitacoes/{id}` | Atualizar completa |
| PATCH | `/solicitacoes/{id}/status` | Atualizar status |
| DELETE | `/solicitacoes/{id}` | Excluir |
| GET | `/solicitacoes/estatisticas/geral` | Estatísticas |

4. **Exemplos de uso com cURL**

**Criar solicitação:**
```bash
curl -X POST "http://localhost:8000/solicitacoes" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "suporte",
    "descricao": "Problema no módulo de autenticação do sistema",
    "status": "pendente"
  }'
```

**Listar todas:**
```bash
curl http://localhost:8000/solicitacoes
```

**Buscar por ID:**
```bash
curl http://localhost:8000/solicitacoes/1
```

**Atualizar status:**
```bash
curl -X PATCH "http://localhost:8000/solicitacoes/1/status?novo_status=em_andamento"
```

**Excluir:**
```bash
curl -X DELETE "http://localhost:8000/solicitacoes/1"
```

### Opção 2: Interface Web (Streamlit)

1. **Certifique-se de que a API está rodando**
```bash
uvicorn app:app --reload
```

2. **Em outro terminal, inicie o Streamlit**
```bash
streamlit run streamlit_app.py
```

3. **Acesse no navegador**
```
http://localhost:8501
```

4. **Funcionalidades da Interface**
- **Dashboard**: Visualize estatísticas em tempo real
- **Nova Solicitação**: Formulário intuitivo para criar
- **Listar**: Visualize e filtre solicitações
- **Atualizar**: Modifique solicitações existentes
- **Excluir**: Remova solicitações com confirmação

## Testes

### Executar todos os testes
```bash
pytest test_api.py -v
```

### Executar com cobertura
```bash
pytest test_api.py --cov=src --cov-report=html
```

### Testes incluídos
- Testes unitários dos modelos
- Testes do repository
- Testes do service
- Testes de integração da API
- Validações de dados
- Casos de erro

## Exemplos de Uso

### Python (usando requests)

```python
import requests

# URL base da API
BASE_URL = "http://localhost:8000"

# Criar solicitação
response = requests.post(f"{BASE_URL}/solicitacoes", json={
    "tipo": "desenvolvimento",
    "descricao": "Implementar novo módulo de relatórios no sistema",
    "status": "pendente"
})
solicitacao = response.json()
print(f"Criada: {solicitacao['id']}")

# Listar todas
response = requests.get(f"{BASE_URL}/solicitacoes")
solicitacoes = response.json()
print(f"Total: {len(solicitacoes)}")

# Atualizar status
solicitacao_id = solicitacao['id']
response = requests.patch(
    f"{BASE_URL}/solicitacoes/{solicitacao_id}/status",
    params={"novo_status": "em_andamento"}
)
print(f"Status atualizado: {response.json()['status']}")

# Excluir
response = requests.delete(f"{BASE_URL}/solicitacoes/{solicitacao_id}")
print(f"Excluída: {response.status_code == 204}")
```

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para APIs
- **Pydantic**: Validação de dados e settings
- **Streamlit**: Framework para criar aplicações web
- **Uvicorn**: Servidor ASGI de alta performance
- **Pytest**: Framework de testes
- **Python 3.8+**: Linguagem de programação

## Estrutura de Dados

### Modelo Solicitacao (JSON)
```json
{
  "id": 1,
  "tipo": "suporte",
  "descricao": "Solicitação de suporte para problema crítico no sistema",
  "status": "pendente",
  "data_criacao": "2025-12-04T10:30:00",
  "data_atualizacao": "2025-12-04T10:30:00"
}
```

## Status Possíveis
- **pendente**: Solicitação criada, aguardando atendimento
- **em_andamento**: Em processo de resolução
- **concluida**: Finalizada com sucesso
- **cancelada**: Cancelada por algum motivo

## Tipos de Solicitação
- **manutencao**: Manutenção preventiva ou corretiva
- **suporte**: Suporte técnico
- **desenvolvimento**: Desenvolvimento de funcionalidades
- **consulta**: Consultas e dúvidas
- **outros**: Outros tipos

## Validações Implementadas

- Descrição com mínimo de 10 e máximo de 500 caracteres
- Tipos e status validados por Enum
- IDs únicos e auto-incrementados
- Timestamps automáticos
- Validação de dados de entrada (Pydantic)
- Tratamento de erros HTTP adequado

## Diferenciais Técnicos

**Arquitetura limpa e escalável**
- Separação de camadas (Models, Repository, Service, Routes)
- Fácil manutenção e extensão

**Documentação automática**
- Swagger UI e ReDoc integrados
- Schemas OpenAPI completos

**Testes abrangentes**
- Cobertura de testes unitários e integração
- Fixtures para testes isolados

**Interface dupla**
- API REST para integração
- UI Web para usuários finais

**Type Safety**
- Type hints completos
- Validação em runtime com Pydantic

**Thread-safe**
- Operações concorrentes seguras
- Lock em operações críticas
