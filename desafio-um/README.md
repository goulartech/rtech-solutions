# API de Controle de Solicitações Internas - RTech

## Descrição

API RESTful desenvolvida com Django e Django REST Framework para gerenciar solicitações internas de uma empresa, incluindo:
- **Férias**: Solicitações de período de férias dos colaboradores
- **Reembolsos**: Solicitações de reembolso de despesas
- **Treinamentos**: Solicitações de participação em treinamentos

## Características

### Funcionalidades Principais
**CRUD Completo**: Criar, Listar, Visualizar, Atualizar e Excluir solicitações  
**Ações de Workflow**: Aprovar, Rejeitar e Cancelar solicitações  
**Filtros Avançados**: Por tipo, status, solicitante, valores e datas  
**Busca**: Pesquisa textual em título, descrição e solicitante  
**Paginação**: Listagem paginada de resultados  
**Ordenação**: Ordenar por múltiplos campos  
**Estatísticas**: Endpoint com métricas agregadas  
**Validações**: Validações robustas em modelo e serializers  
**Documentação**: Swagger/OpenAPI integrado  
**Admin Customizado**: Interface de administração completa  
**Testes**: Cobertura completa de testes unitários e de integração  

### Características Técnicas
- Django 6.0
- Django REST Framework 3.16
- django-filter para filtros avançados
- drf-spectacular para documentação OpenAPI/Swagger
- SQLite (desenvolvimento) - facilmente adaptável para PostgreSQL/MySQL
- Validações customizadas por tipo de solicitação
- Serializers específicos por operação (create, update, list, detail)
- Properties computadas no modelo (duração em dias, permissões)
- Métodos auxiliares no modelo (aprovar, rejeitar, cancelar)

## Instalação

### Pré-requisitos
- Python 3.8+
- pip
- virtualenv (recomendado)

### Passo a Passo

1. **Clone o repositório**
```bash
cd desafio-um
```

2. **Crie e ative o ambiente virtual**
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

4. **Execute as migrations**
```bash
python manage.py migrate
```

5. **Crie um superusuário (opcional)**
```bash
python manage.py createsuperuser
```

6. **Inicie o servidor**
```bash
python manage.py runserver
```

A API estará disponível em: `http://localhost:8000/api/v1/`

## Documentação da API

### Swagger UI (Interativo)
Acesse: `http://localhost:8000/api/docs/`

### Schema OpenAPI
Acesse: `http://localhost:8000/api/schema/`

### Endpoints Disponíveis

#### Solicitações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/solicitacoes/` | Listar todas as solicitações |
| POST | `/api/v1/solicitacoes/` | Criar nova solicitação |
| GET | `/api/v1/solicitacoes/{id}/` | Detalhes de uma solicitação |
| PUT | `/api/v1/solicitacoes/{id}/` | Atualizar solicitação (completo) |
| PATCH | `/api/v1/solicitacoes/{id}/` | Atualizar solicitação (parcial) |
| DELETE | `/api/v1/solicitacoes/{id}/` | Excluir solicitação |
| POST | `/api/v1/solicitacoes/{id}/aprovar/` | Aprovar solicitação |
| POST | `/api/v1/solicitacoes/{id}/rejeitar/` | Rejeitar solicitação |
| POST | `/api/v1/solicitacoes/{id}/cancelar/` | Cancelar solicitação |
| GET | `/api/v1/solicitacoes/estatisticas/` | Obter estatísticas |

### Exemplos de Uso

#### 1. Criar Solicitação de Férias
```bash
curl -X POST http://localhost:8000/api/v1/solicitacoes/ \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "ferias",
    "titulo": "Férias de Verão",
    "descricao": "Férias programadas para janeiro",
    "solicitante": "João Silva",
    "data_inicio": "2025-01-15",
    "data_fim": "2025-01-29"
  }'
```

#### 2. Criar Solicitação de Reembolso
```bash
curl -X POST http://localhost:8000/api/v1/solicitacoes/ \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "reembolso",
    "titulo": "Reembolso de Transporte",
    "descricao": "Despesas com transporte no Projeto X",
    "solicitante": "Maria Santos",
    "valor": "350.00"
  }'
```

#### 3. Criar Solicitação de Treinamento
```bash
curl -X POST http://localhost:8000/api/v1/solicitacoes/ \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "treinamento",
    "titulo": "Curso Django Avançado",
    "descricao": "Treinamento em Django REST Framework",
    "solicitante": "Carlos Souza",
    "valor": "1500.00",
    "data_inicio": "2025-03-10",
    "data_fim": "2025-03-12"
  }'
```

#### 4. Aprovar Solicitação
```bash
curl -X POST http://localhost:8000/api/v1/solicitacoes/1/aprovar/ \
  -H "Content-Type: application/json" \
  -d '{
    "observacoes": "Aprovado pela gerência"
  }'
```

#### 5. Filtrar por Tipo
```bash
curl http://localhost:8000/api/v1/solicitacoes/?tipo=ferias
```

#### 6. Filtrar por Status
```bash
curl http://localhost:8000/api/v1/solicitacoes/?status=pendente
```

#### 7. Buscar por Solicitante
```bash
curl http://localhost:8000/api/v1/solicitacoes/?search=Maria
```

#### 8. Obter Estatísticas
```bash
curl http://localhost:8000/api/v1/solicitacoes/estatisticas/
```

### Script Python de Exemplo

Execute o script de exemplo incluído:

```bash
python exemplo_uso_api.py
```

## Testes

Execute os testes com:

```bash
python manage.py test
```

Para executar com relatório de cobertura:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Cobertura de Testes

Os testes cobrem:
- Validações do modelo
- Métodos do modelo (aprovar, rejeitar, cancelar)
- CRUD completo via API
- Ações customizadas (aprovar, rejeitar, cancelar)
- Filtros e buscas
- Paginação
- Validações de regras de negócio
- Tratamento de erros

## Configurações

### Paginação

A paginação está configurada globalmente em `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Filtros Disponíveis

- `tipo`: Tipo de solicitação (ferias, reembolso, treinamento)
- `status`: Status (pendente, em_analise, aprovado, rejeitado, cancelado)
- `solicitante`: Nome do solicitante (busca case-insensitive)
- `data_criacao_min` / `data_criacao_max`: Faixa de data de criação
- `data_inicio_min` / `data_inicio_max`: Faixa de data de início
- `valor_min` / `valor_max`: Faixa de valores
- `search`: Busca textual em título, descrição e solicitante
- `ordering`: Ordenar por campos (data_criacao, data_atualizacao, data_inicio, valor)

Exemplo: `/api/v1/solicitacoes/?tipo=reembolso&status=pendente&valor_min=100&ordering=-data_criacao`

## Django Admin

Acesse o painel administrativo em: `http://localhost:8000/admin/`

Features do Admin:
- Lista com filtros laterais
- Busca integrada
- Ações em massa (aprovar, rejeitar, cancelar)
- Status com badges coloridos
- Campos calculados exibidos
- Organização em fieldsets

## Modelo de Dados

### Request (Solicitação)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | ID único (auto-incremento) |
| tipo | String | Tipo: ferias, reembolso, treinamento |
| titulo | String | Título descritivo |
| descricao | Text | Descrição detalhada |
| status | String | Status: pendente, em_analise, aprovado, rejeitado, cancelado |
| valor | Decimal | Valor monetário (obrigatório para reembolso e treinamento) |
| data_inicio | Date | Data de início (obrigatório para férias e treinamento) |
| data_fim | Date | Data de término (obrigatório para férias e treinamento) |
| solicitante | String | Nome do solicitante |
| observacoes | Text | Observações adicionais |
| data_criacao | DateTime | Data/hora de criação (auto) |
| data_atualizacao | DateTime | Data/hora de atualização (auto) |

### Regras de Negócio

1. **Férias**:
   - Requer `data_inicio` e `data_fim`
   - `data_fim` deve ser posterior a `data_inicio`
   - Campo `valor` é opcional

2. **Reembolso**:
   - Requer `valor` (> 0)
   - Campos `data_inicio` e `data_fim` são opcionais

3. **Treinamento**:
   - Requer `valor` (> 0)
   - Requer `data_inicio` e `data_fim`
   - `data_fim` deve ser posterior a `data_inicio`

4. **Aprovação/Rejeição**:
   - Apenas solicitações com status `pendente` ou `em_analise` podem ser aprovadas/rejeitadas

5. **Cancelamento**:
   - Apenas solicitações com status `pendente` ou `em_analise` podem ser canceladas

6. **Atualização**:
   - Solicitações com status `aprovado`, `rejeitado` ou `cancelado` não podem ser atualizadas

7. **Exclusão**:
   - Solicitações com status `aprovado` não podem ser excluídas

## Arquitetura

```
desafio-um/
├── core/                      # Configurações do projeto
│   ├── settings.py           # Configurações gerais
│   ├── urls.py               # URLs principais
│   └── wsgi.py
├── solicitations/            # App de solicitações
│   ├── models.py            # Modelo Request
│   ├── serializers.py       # Serializers DRF
│   ├── views.py             # ViewSets
│   ├── urls.py              # Rotas da API
│   ├── filters.py           # Filtros customizados
│   ├── admin.py             # Configuração do Admin
│   ├── tests.py             # Testes
│   └── migrations/          # Migrations do banco
├── manage.py                # CLI do Django
├── requirements.txt         # Dependências
├── exemplo_uso_api.py       # Script de exemplo
└── README.md               # Este arquivo
```
