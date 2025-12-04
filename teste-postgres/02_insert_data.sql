-- ============================================================================
-- PROVA DE PROFICIÊNCIA EM BANCO DE DADOS - POSTGRESQL
-- Sistema de Auxílio Transporte
-- Arquivo: 02_insert_data.sql
-- Descrição: Carga de dados inicial do sistema
-- ============================================================================

-- ============================================================================
-- 1. INSERÇÃO DE FUNCIONÁRIOS (20 registros)
-- ============================================================================

INSERT INTO funcionarios (nome, matricula, departamento, data_admissao) VALUES
('Carlos Silva Santos', 'FUNC001', 'TI', '2020-03-15'),
('Maria Oliveira Costa', 'FUNC002', 'RH', '2019-07-22'),
('João Pedro Almeida', 'FUNC003', 'Financeiro', '2021-01-10'),
('Ana Paula Ferreira', 'FUNC004', 'Operações', '2020-11-05'),
('Roberto Carlos Lima', 'FUNC005', 'Marketing', '2022-02-18'),
('Juliana Santos Rocha', 'FUNC006', 'TI', '2021-06-30'),
('Fernando Henrique Dias', 'FUNC007', 'RH', '2020-09-12'),
('Patricia Souza Martins', 'FUNC008', 'Financeiro', '2019-04-25'),
('Ricardo Alves Pereira', 'FUNC009', 'Operações', '2021-08-17'),
('Camila Rodrigues Silva', 'FUNC010', 'Marketing', '2022-05-03'),
('Bruno Costa Mendes', 'FUNC011', 'TI', '2020-12-08'),
('Fernanda Lima Santos', 'FUNC012', 'RH', '2021-03-20'),
('Gustavo Oliveira Souza', 'FUNC013', 'Financeiro', '2019-10-14'),
('Mariana Ferreira Costa', 'FUNC014', 'Operações', '2022-01-28'),
('Diego Santos Almeida', 'FUNC015', 'Marketing', '2020-07-09'),
('Beatriz Rocha Silva', 'FUNC016', 'TI', '2021-11-15'),
('Lucas Martins Pereira', 'FUNC017', 'RH', '2020-05-22'),
('Aline Costa Rodrigues', 'FUNC018', 'Financeiro', '2022-03-11'),
('Rafael Souza Lima', 'FUNC019', 'Operações', '2019-12-06'),
('Larissa Alves Santos', 'FUNC020', 'Marketing', '2021-09-24');

-- Verificar inserção
SELECT COUNT(*) as total_funcionarios FROM funcionarios;
SELECT departamento, COUNT(*) as qtd_por_depto FROM funcionarios GROUP BY departamento;

-- ============================================================================
-- 2. INSERÇÃO DE SOLICITAÇÕES (25 registros com datas variadas)
-- ============================================================================

-- Solicitações dos últimos 6 meses (maioria APROVADO)
INSERT INTO solicitacoes (funcionario_id, valor_solicitado, data_solicitacao, status, observacao) VALUES
(1, 250.00, '2025-11-15 09:30:00', 'APROVADO', 'Transporte para projeto urgente'),
(2, 180.00, '2025-11-10 14:20:00', 'APROVADO', 'Deslocamento reunião cliente'),
(3, 320.00, '2025-10-25 10:15:00', 'APROVADO', 'Viagem a trabalho'),
(4, 150.00, '2025-10-20 16:45:00', 'APROVADO', 'Transporte extra turno'),
(5, 420.00, '2025-10-18 08:00:00', 'APROVADO', 'Deslocamento para treinamento'),
(6, 280.00, '2025-09-30 11:30:00', 'APROVADO', 'Reunião com fornecedor'),
(7, 195.00, '2025-09-25 13:15:00', 'APROVADO', 'Visita técnica'),
(8, 350.00, '2025-09-20 09:45:00', 'APROVADO', 'Auditoria externa'),
(9, 220.00, '2025-08-28 15:20:00', 'APROVADO', 'Treinamento operacional'),
(10, 310.00, '2025-08-15 10:00:00', 'APROVADO', 'Evento de marketing'),
(11, 240.00, '2025-07-30 14:30:00', 'APROVADO', 'Implementação de sistema'),
(12, 175.00, '2025-07-22 08:45:00', 'APROVADO', 'Recrutamento externo'),
(13, 290.00, '2025-11-20 16:00:00', 'APROVADO', 'Fechamento fiscal'),
(14, 200.00, '2025-11-18 12:30:00', 'APROVADO', 'Supervisão de obra'),
(15, 380.00, '2025-11-12 09:15:00', 'APROVADO', 'Campanha publicitária'),
(16, 265.00, '2025-10-28 11:00:00', 'APROVADO', 'Manutenção servidor'),
(17, 185.00, '2025-10-15 15:45:00', 'APROVADO', 'Processo seletivo'),
(18, 340.00, '2025-09-18 10:30:00', 'APROVADO', 'Análise financeira'),
(19, 215.00, '2025-08-20 14:15:00', 'APROVADO', 'Logística de entrega'),
(20, 295.00, '2025-07-25 08:30:00', 'APROVADO', 'Pesquisa de mercado'),

-- Solicitações mais antigas e outros status
(1, 160.00, '2025-05-10 09:00:00', 'PAGO', 'Transporte mensal'),
(5, 190.00, '2025-04-15 13:30:00', 'CANCELADO', 'Reunião cancelada'),
(10, 275.00, '2025-03-20 11:45:00', 'PENDENTE', 'Aguardando aprovação'),
(15, 230.00, '2025-02-28 16:20:00', 'CANCELADO', 'Viagem remarcada'),
(8, 410.00, '2025-01-12 10:10:00', 'PAGO', 'Consultoria externa');

-- Verificar inserção
SELECT COUNT(*) as total_solicitacoes FROM solicitacoes;
SELECT status, COUNT(*) as qtd_por_status FROM solicitacoes GROUP BY status;
SELECT DATE_TRUNC('month', data_solicitacao) as mes, COUNT(*) as qtd 
FROM solicitacoes 
GROUP BY mes 
ORDER BY mes DESC;

-- ============================================================================
-- 3. INSERÇÃO DE PAGAMENTOS (20 registros)
-- ============================================================================

-- Pagamentos referentes às solicitações APROVADAS
INSERT INTO pagamentos (solicitacao_id, valor_pago, data_pagamento, forma_pagamento) VALUES
(1, 250.00, '2025-11-20 10:00:00', 'PIX'),
(2, 180.00, '2025-11-15 14:30:00', 'TED'),
(3, 320.00, '2025-11-01 09:15:00', 'PIX'),
(4, 150.00, '2025-10-25 11:45:00', 'DINHEIRO'),
(5, 420.00, '2025-10-23 15:20:00', 'TED'),
(6, 280.00, '2025-10-05 10:30:00', 'PIX'),
(7, 195.00, '2025-09-30 13:00:00', 'PIX'),
(8, 350.00, '2025-09-25 16:15:00', 'TED'),
(9, 220.00, '2025-09-03 09:45:00', 'PIX'),
(10, 310.00, '2025-08-20 14:00:00', 'TED'),
(11, 240.00, '2025-08-05 11:30:00', 'PIX'),
(12, 175.00, '2025-07-28 10:15:00', 'DINHEIRO'),
(13, 290.00, '2025-11-25 15:45:00', 'PIX'),
(14, 200.00, '2025-11-22 12:00:00', 'TED'),
(15, 380.00, '2025-11-17 09:30:00', 'PIX'),
(16, 265.00, '2025-11-02 14:45:00', 'TED'),
(17, 185.00, '2025-10-20 11:15:00', 'PIX'),
(18, 340.00, '2025-09-23 16:30:00', 'TED'),
(19, 215.00, '2025-08-25 10:45:00', 'PIX'),
(20, 295.00, '2025-07-30 13:20:00', 'DINHEIRO');

-- Verificar inserção
SELECT COUNT(*) as total_pagamentos FROM pagamentos;
SELECT forma_pagamento, COUNT(*) as qtd FROM pagamentos GROUP BY forma_pagamento;

-- ============================================================================
-- 4. INSERÇÃO DE LOGS DE AUDITORIA
-- ============================================================================

INSERT INTO log_auditoria (tabela_afetada, operacao, registro_id, detalhes) VALUES
('funcionarios', 'INSERT', 1, 'Cadastro inicial de funcionários'),
('solicitacoes', 'INSERT', 1, 'Primeira solicitação registrada no sistema'),
('solicitacoes', 'UPDATE', 22, 'Status alterado para CANCELADO - Reunião cancelada'),
('solicitacoes', 'UPDATE', 24, 'Status alterado para CANCELADO - Viagem remarcada'),
('pagamentos', 'INSERT', 1, 'Primeiro pagamento processado via PIX');

-- Verificar inserção
SELECT COUNT(*) as total_logs FROM log_auditoria;

-- ============================================================================
-- VERIFICAÇÕES FINAIS
-- ============================================================================

-- Resumo geral dos dados
SELECT 
    'Funcionários' as tabela, 
    COUNT(*) as total 
FROM funcionarios
UNION ALL
SELECT 
    'Solicitações', 
    COUNT(*) 
FROM solicitacoes
UNION ALL
SELECT 
    'Pagamentos', 
    COUNT(*) 
FROM pagamentos
UNION ALL
SELECT 
    'Logs de Auditoria', 
    COUNT(*) 
FROM log_auditoria;

-- Verificar solicitações dos últimos 6 meses
SELECT 
    COUNT(*) as solicitacoes_ultimos_6_meses
FROM solicitacoes
WHERE data_solicitacao >= CURRENT_DATE - INTERVAL '6 months';

-- Verificar solicitações aprovadas sem pagamento
SELECT 
    s.id, 
    s.funcionario_id, 
    s.valor_solicitado, 
    s.status
FROM solicitacoes s
LEFT JOIN pagamentos p ON s.id = p.solicitacao_id
WHERE s.status = 'APROVADO' AND p.id IS NULL;
