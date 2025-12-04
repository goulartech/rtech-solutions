# Sistema de Gerenciamento de Notas

Sistema completo de CRUD para gerenciar alunos e suas notas, desenvolvido com React, TypeScript e Tailwind CSS.

## Funcionalidades

### Gerenciamento de Alunos
- **Criar** novos alunos com validação de dados
- **Editar** informações dos alunos cadastrados
- **Excluir** alunos do sistema
- **Buscar** alunos por nome, email ou matrícula
- **Visualizar** média geral de cada aluno

### Gerenciamento de Notas
- **Adicionar** notas para cada disciplina
- **Editar** notas existentes
- **Excluir** notas específicas
- **Cálculo automático** da média geral
- **Indicadores visuais** de desempenho (verde ≥7, amarelo ≥5, vermelho <5)

## Tecnologias Utilizadas

- **React 18** - Biblioteca JavaScript para construção de interfaces
- **TypeScript** - Superset JavaScript com tipagem estática
- **Vite** - Build tool moderna e rápida
- **Tailwind CSS** - Framework CSS utility-first
- **Context API** - Gerenciamento de estado global
- **Custom Hooks** - Lógica reutilizável e organizada

## Pré-requisitos

- Node.js 16+ instalado
- npm ou yarn

## Instalação e Execução

### 1. Instalar dependências
```bash
npm install
```

### 2. Executar em modo de desenvolvimento
```bash
npm run dev
```

### 3. Acessar a aplicação
Abra o navegador em: `http://localhost:5173`

### 4. Build para produção
```bash
npm run build
```

### 5. Preview do build
```bash
npm run preview
```

## Estrutura do Projeto

```
src/
├── components/           # Componentes React
│   ├── StudentCard/     # Card individual do aluno
│   ├── StudentForm/     # Formulário de cadastro/edição
│   └── StudentList/     # Lista e busca de alunos
├── contexts/            # Context API para estado global
│   └── StudentsContext.tsx
├── types/               # Definições TypeScript
│   └── index.ts
├── utils/               # Funções utilitárias
│   └── helpers.ts
├── App.tsx              # Componente principal
└── main.tsx             # Ponto de entrada
```

## Arquitetura e Boas Práticas

### Padrões Implementados
- **Separation of Concerns**: Separação clara entre lógica e apresentação
- **Component Composition**: Componentes reutilizáveis e modulares
- **Type Safety**: Uso extensivo de TypeScript para prevenção de erros
- **Custom Hooks**: Encapsulamento de lógica complexa
- **Context API**: Estado global sem prop drilling
- **Immutability**: Atualizações imutáveis de estado
- **Validation**: Validação de formulários e dados

### Validações Implementadas
- Nome: obrigatório e não vazio
- Email: formato válido e obrigatório
- Matrícula: obrigatória e não vazia
- Disciplina: obrigatória para notas
- Nota: deve estar entre 0 e 10

## Interface e UX

### Características
- **Design Responsivo**: Funciona em mobile, tablet e desktop
- **Feedback Visual**: Cores indicando desempenho dos alunos
- **Confirmações**: Alertas antes de ações destrutivas
- **Loading States**: Feedback visual durante operações
- **Empty States**: Mensagens claras quando não há dados
- **Validação em Tempo Real**: Feedback imediato em formulários

### Paleta de Cores
- **Primary**: Azul (#3b82f6) - Ações principais
- **Success**: Verde - Notas boas (≥7.0)
- **Warning**: Amarelo - Notas regulares (≥5.0 e <7.0)
- **Danger**: Vermelho - Notas baixas (<5.0)

## Screenshots

![Screenshot 1](screenshots/desafio-tres%201.png)

![Screenshot 2](screenshots/desafio-tres%202.png)

## Armazenamento

Os dados são mantidos **em memória** durante a sessão.

## Testando a Aplicação

### Dados de Exemplo
A aplicação já vem com 2 alunos pré-cadastrados para demonstração:
- Ana Silva (Matrícula: 2024001)
- Carlos Oliveira (Matrícula: 2024002)

### Fluxo de Teste
1. **Visualizar** alunos existentes na página inicial
2. **Buscar** aluno digitando no campo de busca
3. **Adicionar** novo aluno clicando em "Novo Aluno"
4. **Editar** aluno clicando no ícone de lápis
5. **Adicionar nota** clicando em "Adicionar Nota" no card do aluno
6. **Editar/Excluir nota** usando os ícones ao lado de cada nota
7. **Excluir aluno** clicando no ícone de lixeira
