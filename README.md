# RTech Solutions - Processo Seletivo

Repositório desenvolvido para processo seletivo de **Desenvolvedor Fullstack Pleno**, contendo 3 desafios práticos, questões teóricas e teste de banco de dados.

## Estrutura do Projeto

### Desafios Práticos

#### **Desafio 1** - API de Solicitações com Django REST Framework
Sistema completo de gerenciamento de solicitações internas (férias, reembolsos, treinamentos) com:
- CRUD completo e ações de workflow (aprovar, rejeitar, cancelar)
- Filtros avançados, busca e paginação
- Documentação Swagger/OpenAPI integrada
- Testes unitários e de integração
- Django Admin customizado

🔗 [Ver detalhes](./desafio-um/README.md)

#### **Desafio 2** - Sistema de Solicitações com FastAPI + Streamlit
Aplicação dupla interface implementando Clean Architecture:
- API REST com FastAPI (documentação automática)
- Interface Web com Streamlit
- Repository Pattern e Service Layer
- Validações com Pydantic
- Testes automatizados

🔗 [Ver detalhes](./desafio-dois/README.md)

#### **Desafio 3** - CRUD de Notas com React + TypeScript
Sistema de gerenciamento de alunos e notas com interface moderna:
- React 18 + TypeScript + Tailwind CSS
- Context API para estado global
- Custom Hooks e validações em tempo real
- Design responsivo e indicadores visuais de desempenho
- Componentização modular

[Ver detalhes](./desafio-tres/README.md)

---

### Questões Teóricas

#### **Backend**
Respostas sobre REST vs SOAP, HTTP status codes, SOLID, arquitetura de projetos, tratamento de exceções e testes unitários.

[Ver respostas](./perguntas-backend/respostas.md)

#### **Frontend**
Respostas sobre DOM, JavaScript, React Hooks, CSS Box Model, Promises, componentes funcionais e gerenciamento de estado.

[Ver respostas](./perguntas-frontend/respostas.md)

---

### Teste PostgreSQL

Sistema de auxílio transporte com:
- Modelagem de 4 tabelas (funcionários, solicitações, pagamentos, auditoria)
- Consultas com JOIN, GROUP BY e HAVING
- Trigger automático para atualização de status
- Stored Procedure com validações
- Window Functions para ranking

[Ver implementação](./teste-postgres/)

---

## Tecnologias Utilizadas

### Backend
- Python 3.8+ (Django 6.0, FastAPI, Pydantic)
- Django REST Framework
- SQLite / PostgreSQL
- Pytest

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Context API

### Banco de Dados
- PostgreSQL
- Triggers e Stored Procedures
- Window Functions

---

## Como Executar

Cada desafio possui seu próprio README com instruções detalhadas de instalação e execução.

### Exemplo rápido:

```bash
# Desafio 1 (Django)
cd desafio-um
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Desafio 2 (FastAPI + Streamlit)
cd desafio-dois
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
streamlit run streamlit_app.py  # Em outro terminal

# Desafio 3 (React)
cd desafio-tres
npm install
npm run dev
```

---

## Diferenciais Técnicos

**Arquitetura Limpa**: Separação de camadas e responsabilidades  
**Clean Code**: Código legível, tipado e bem documentado  
**Testes Automatizados**: Cobertura de testes unitários e integração  
**Documentação**: READMEs detalhados e comentários no código  
**Boas Práticas**: SOLID, Design Patterns, Validações robustas  
**UX/UI**: Interfaces intuitivas e responsivas  
**Type Safety**: TypeScript no frontend e Type Hints no backend

---

## Estrutura do Repositório

```
rtech-solutions/
├── desafio-um/           # Django REST API
├── desafio-dois/         # FastAPI + Streamlit
├── desafio-tres/         # React + TypeScript
├── perguntas-backend/    # Questões teóricas backend
├── perguntas-frontend/   # Questões teóricas frontend
├── teste-postgres/       # Scripts SQL PostgreSQL
└── README.md            # Este arquivo
```

---

## Contato

Desenvolvido por **Luiz** - Desenvolvedor Fullstack Pleno

---

**Nota**: Este repositório foi desenvolvido exclusivamente para avaliação técnica do processo seletivo da RTech Solutions.
