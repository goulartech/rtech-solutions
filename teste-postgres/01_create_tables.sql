-- ============================================================================
-- PROVA DE PROFICIÊNCIA EM BANCO DE DADOS - POSTGRESQL
-- Sistema de Auxílio Transporte
-- Arquivo: 01_create_tables.sql
-- Descrição: Criação das tabelas do sistema
-- ============================================================================

-- Conectar ao banco de dados
-- Execute no terminal: psql -U postgres
-- Depois: CREATE DATABASE prova_banco_dados;
-- Depois: \c prova_banco_dados

-- ============================================================================
-- 1. TABELA DE FUNCIONÁRIOS
-- ============================================================================

CREATE TABLE funcionarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    data_admissao DATE NOT NULL
);

COMMENT ON TABLE funcionarios IS 'Armazena informações dos colaboradores da empresa';
COMMENT ON COLUMN funcionarios.matricula IS 'Matrícula única do funcionário';
COMMENT ON COLUMN funcionarios.departamento IS 'Departamento onde o funcionário trabalha';

-- ============================================================================
-- 2. TABELA DE SOLICITAÇÕES DE AUXÍLIO
-- ============================================================================

CREATE TABLE solicitacoes (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER NOT NULL,
    valor_solicitado NUMERIC(10,2) NOT NULL CHECK (valor_solicitado > 0),
    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'PENDENTE' CHECK (status IN ('PENDENTE', 'APROVADO', 'CANCELADO', 'PAGO')),
    observacao TEXT,
    CONSTRAINT fk_funcionario 
        FOREIGN KEY (funcionario_id) 
        REFERENCES funcionarios(id)
        ON DELETE RESTRICT
);

COMMENT ON TABLE solicitacoes IS 'Registra pedidos de auxílio transporte dos funcionários';
COMMENT ON COLUMN solicitacoes.status IS 'Status: PENDENTE, APROVADO, CANCELADO, PAGO';
COMMENT ON COLUMN solicitacoes.valor_solicitado IS 'Valor do auxílio solicitado (deve ser maior que 0)';

-- ============================================================================
-- 3. TABELA DE PAGAMENTOS
-- ============================================================================

CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    solicitacao_id INTEGER UNIQUE NOT NULL,
    valor_pago NUMERIC(10,2) NOT NULL CHECK (valor_pago > 0),
    data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    forma_pagamento VARCHAR(20) NOT NULL,
    CONSTRAINT fk_solicitacao 
        FOREIGN KEY (solicitacao_id) 
        REFERENCES solicitacoes(id)
        ON DELETE RESTRICT
);

COMMENT ON TABLE pagamentos IS 'Registra os pagamentos realizados das solicitações aprovadas';
COMMENT ON COLUMN pagamentos.solicitacao_id IS 'Referência única à solicitação (uma solicitação só pode ter um pagamento)';
COMMENT ON COLUMN pagamentos.forma_pagamento IS 'Método de pagamento: PIX, TED, DINHEIRO';

-- ============================================================================
-- 4. TABELA DE LOG DE AUDITORIA
-- ============================================================================

CREATE TABLE log_auditoria (
    id SERIAL PRIMARY KEY,
    tabela_afetada VARCHAR(50) NOT NULL,
    operacao VARCHAR(20) NOT NULL CHECK (operacao IN ('INSERT', 'UPDATE', 'DELETE')),
    registro_id INTEGER,
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalhes TEXT
);

COMMENT ON TABLE log_auditoria IS 'Mantém histórico de operações críticas do sistema';
COMMENT ON COLUMN log_auditoria.operacao IS 'Tipo de operação: INSERT, UPDATE, DELETE';
COMMENT ON COLUMN log_auditoria.detalhes IS 'Informações adicionais sobre a operação';

-- ============================================================================
-- ÍNDICES PARA OTIMIZAÇÃO
-- ============================================================================

-- Índice para consultas por departamento
CREATE INDEX idx_funcionarios_departamento ON funcionarios(departamento);

-- Índice para consultas por status e data
CREATE INDEX idx_solicitacoes_status ON solicitacoes(status);
CREATE INDEX idx_solicitacoes_data ON solicitacoes(data_solicitacao DESC);

-- Índice para consultas de auditoria
CREATE INDEX idx_log_tabela_operacao ON log_auditoria(tabela_afetada, operacao);

-- ============================================================================
-- VERIFICAÇÃO
-- ============================================================================

-- Listar todas as tabelas criadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
