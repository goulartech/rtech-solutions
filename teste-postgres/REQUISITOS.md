# Requisitos - Teste PostgreSQL: Sistema de Auxílio Transporte

## Visão Geral
Desenvolver um sistema de banco de dados PostgreSQL para gerenciar solicitações de auxílio transporte de funcionários, incluindo controle de pagamentos e auditoria.

---

## 1. Modelagem de Dados

### 1.1 Tabela: funcionarios
**Objetivo:** Armazenar informações dos colaboradores da empresa.

**Campos necessários:**
- `id`: Identificador único (chave primária, serial)
- `nome`: Nome completo do funcionário (obrigatório)
- `matricula`: Matrícula única do funcionário (obrigatório, único)
- `departamento`: Setor onde trabalha (obrigatório)
- `data_admissao`: Data de entrada na empresa

**Validações:**
- Matrícula deve ser única
- Nome e departamento não podem ser nulos

---

### 1.2 Tabela: solicitacoes
**Objetivo:** Registrar pedidos de auxílio transporte dos funcionários.

**Campos necessários:**
- `id`: Identificador único (chave primária, serial)
- `funcionario_id`: Referência ao funcionário (foreign key)
- `valor_solicitado`: Valor do auxílio solicitado (obrigatório)
- `data_solicitacao`: Data/hora da solicitação (default: data atual)
- `status`: Estado da solicitação (PENDENTE, APROVADO, CANCELADO, PAGO)
- `observacao`: Campo opcional para anotações

**Validações:**
- funcionario_id deve existir na tabela funcionarios
- valor_solicitado deve ser maior que 0
- status deve ter valor padrão 'PENDENTE'

---

### 1.3 Tabela: pagamentos
**Objetivo:** Registrar os pagamentos realizados das solicitações aprovadas.

**Campos necessários:**
- `id`: Identificador único (chave primária, serial)
- `solicitacao_id`: Referência à solicitação (foreign key, único)
- `valor_pago`: Valor efetivamente pago
- `data_pagamento`: Data do pagamento (default: data atual)
- `forma_pagamento`: Método utilizado (ex: PIX, TED, DINHEIRO)

**Validações:**
- solicitacao_id deve existir e ser único (uma solicitação só pode ter um pagamento)
- valor_pago deve ser maior que 0

---

### 1.4 Tabela: log_auditoria
**Objetivo:** Manter histórico de operações críticas do sistema.

**Campos necessários:**
- `id`: Identificador único (chave primária, serial)
- `tabela_afetada`: Nome da tabela que sofreu alteração
- `operacao`: Tipo de operação (INSERT, UPDATE, DELETE)
- `registro_id`: ID do registro afetado
- `data_operacao`: Data/hora da operação (default: data atual)
- `detalhes`: Informações adicionais sobre a operação

---

## 2. Carga de Dados

### 2.1 Funcionários (20 registros)
- Distribuir entre diferentes departamentos (TI, RH, Financeiro, Operações, Marketing)
- Usar matrículas sequenciais ou padronizadas
- Variar datas de admissão

### 2.2 Solicitações (25 registros)
- Distribuir entre os funcionários cadastrados
- Variar valores (ex: 100 a 500)
- Incluir diferentes status (maioria APROVADO)
- Espalhar datas nos últimos 12 meses

### 2.3 Pagamentos (20 registros)
- Vincular a solicitações com status APROVADO
- Valores devem corresponder aos solicitados
- Variar formas de pagamento

### 2.4 Logs de Auditoria
- Registrar operações relevantes realizadas

---

## 3. Consultas e Lógica de Negócio

### 3.1 Questão 1: Relatório de Solicitações Aprovadas (2,0 pontos)
**Objetivo:** Listar solicitações aprovadas recentes com ordenação específica.

**Requisitos técnicos:**
- INNER JOIN entre funcionarios e solicitacoes
- Filtro: status = 'APROVADO'
- Filtro: data_solicitacao >= (data_atual - 6 meses)
- ORDER BY: departamento ASC, valor_solicitado DESC

**Campos retornados:**
- nome, matricula, departamento, valor_solicitado, status, data_solicitacao

---

### 3.2 Questão 2: Análise Mensal Agregada (2,0 pontos)
**Objetivo:** Gerar relatório estatístico mensal de solicitações.

**Requisitos técnicos:**
- GROUP BY: ano e mês da solicitação
- HAVING: quantidade de solicitações > 10
- ORDER BY: data decrescente (mais recente primeiro)
- Funções agregadas: COUNT, SUM, AVG
- Formatar ano/mês como 'YYYY-MM'

**Campos retornados:**
- ano_mes, total_solicitacoes, valor_total, valor_medio, qtd_aprovadas

**Observação:** Pode ser necessário ajustar os dados para ter meses com mais de 10 solicitações.

---

### 3.3 Questão 3: Trigger de Pagamento (2,0 pontos)
**Objetivo:** Automatizar atualização de status quando pagamento é registrado.

**Requisitos técnicos:**
- Criar função trigger
- Momento: AFTER INSERT na tabela pagamentos
- Ação 1: UPDATE solicitacoes SET status = 'PAGO' WHERE id = NEW.solicitacao_id
- Ação 2: INSERT em log_auditoria com detalhes da operação
- Usar NEW para acessar dados do registro inserido

**Estrutura:**
1. Criar função que retorna TRIGGER
2. Criar trigger que chama a função

---

### 3.4 Questão 4: Stored Procedure de Cancelamento (2,0 pontos)
**Objetivo:** Criar procedimento seguro para cancelar solicitações.

**Requisitos técnicos:**
- Nome: sp_cancelar_solicitacao
- Parâmetros: p_solicitacao_id, p_motivo
- Validação: verificar se status != 'PAGO'
- Ação 1: UPDATE solicitacoes SET status = 'CANCELADO'
- Ação 2: INSERT em log_auditoria
- Retorno: mensagem de sucesso ou erro

**Controle de fluxo:**
- IF status = 'PAGO' THEN lançar exceção ou retornar erro
- ELSE executar cancelamento e registrar log

---

### 3.5 Questão 5: Ranking com Window Functions (2,0 pontos)
**Objetivo:** Identificar top 3 funcionários por departamento em gastos.

**Requisitos técnicos:**
- JOIN: funcionarios + solicitacoes + pagamentos
- Filtro: status = 'APROVADO' e pagamento existe
- Window Function: ROW_NUMBER() OVER (PARTITION BY departamento ORDER BY total_gasto DESC)
- GROUP BY: funcionário
- HAVING: ranking <= 3
- Calcular percentual do total do departamento

**Campos retornados:**
- nome, departamento, total_gasto, qtd_solicitacoes, ranking, percentual_departamento

**Cálculo do percentual:**
- (total_gasto_funcionario / total_gasto_departamento) * 100
- Usar subquery ou CTE para calcular total por departamento

---

## 4. Testes e Validações

### 4.1 Teste da Procedure
- Executar: `SELECT sp_cancelar_solicitacao(id_valido, 'Teste de cancelamento');`
- Verificar retorno da mensagem
- Confirmar atualização do status
- Verificar registro no log

### 4.2 Teste do Trigger
- Inserir novo pagamento: `INSERT INTO pagamentos (...) VALUES (...);`
- Verificar se status da solicitação mudou para 'PAGO'
- Consultar log_auditoria para confirmar registro

### 4.3 Cenários de Teste Adicionais
- Tentar cancelar solicitação já paga (deve falhar)
- Inserir pagamento duplicado (deve falhar por constraint UNIQUE)
- Consultar relatórios com diferentes períodos

---

## 5. Estrutura de Entrega

Organizar os arquivos SQL da seguinte forma:

1. **01_create_tables.sql** - DDL das tabelas
2. **02_insert_data.sql** - Carga de dados inicial
3. **03_questao_01.sql** - Consulta com JOIN
4. **04_questao_02.sql** - Consulta com GROUP BY
5. **05_questao_03.sql** - Trigger
6. **06_questao_04.sql** - Stored Procedure
7. **07_questao_05.sql** - Window Functions
8. **08_testes.sql** - Scripts de validação

---

## 6. Critérios de Avaliação

- **Modelagem:** Integridade referencial, tipos de dados adequados, constraints
- **Consultas:** Eficiência, clareza, atendimento aos requisitos
- **Trigger:** Funcionamento correto, tratamento de erros
- **Procedure:** Validações, lógica de negócio, retorno adequado
- **Window Functions:** Uso correto de PARTITION BY, cálculos precisos
- **Código:** Legibilidade, comentários, boas práticas SQL

---

## Observações Finais

- Usar nomenclatura em português conforme padrão do teste
- Testar todos os scripts antes da entrega
- Documentar decisões técnicas quando necessário
- Garantir que os scripts sejam executáveis em ordem
