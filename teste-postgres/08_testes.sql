-- ============================================================================
-- PROVA DE PROFICIÊNCIA EM BANCO DE DADOS - POSTGRESQL
-- Sistema de Auxílio Transporte
-- Arquivo: 08_testes.sql
-- Descrição: Scripts de validação e testes do sistema
-- ============================================================================

-- ============================================================================
-- 1. TESTE DA STORED PROCEDURE (QUESTÃO 4)
-- ============================================================================

-- Teste 1: Cancelar solicitação válida (status PENDENTE)
SELECT sp_cancelar_solicitacao(23, 'Teste de cancelamento - solicitação em análise');

-- Verificar se o status foi alterado
SELECT id, funcionario_id, valor_solicitado, status, observacao
FROM solicitacoes
WHERE id = 23;

-- Verificar registro no log de auditoria
SELECT *
FROM log_auditoria
WHERE tabela_afetada = 'solicitacoes' 
  AND registro_id = 23
ORDER BY data_operacao DESC
LIMIT 1;

-- Teste 2: Tentar cancelar solicitação já PAGA (deve retornar erro)
SELECT sp_cancelar_solicitacao(21, 'Tentativa de cancelar solicitação paga');

-- Teste 3: Tentar cancelar solicitação inexistente
SELECT sp_cancelar_solicitacao(9999, 'Teste com ID inexistente');

-- Teste 4: Cancelar solicitação APROVADA
SELECT sp_cancelar_solicitacao(2, 'Mudança de planos - não será necessário deslocamento');

-- Verificar resultado
SELECT id, funcionario_id, valor_solicitado, status, observacao
FROM solicitacoes
WHERE id = 2;

-- ============================================================================
-- 2. TESTE DO TRIGGER (QUESTÃO 3)
-- ============================================================================

-- Verificar solicitações APROVADAS sem pagamento
SELECT s.id, s.funcionario_id, s.valor_solicitado, s.status
FROM solicitacoes s
LEFT JOIN pagamentos p ON s.id = p.solicitacao_id
WHERE s.status = 'APROVADO' AND p.id IS NULL
LIMIT 5;

-- Limpar pagamentos de teste anteriores (se existirem)
DELETE FROM pagamentos WHERE solicitacao_id IN (3, 4);
UPDATE solicitacoes SET status = 'APROVADO' WHERE id IN (3, 4);

-- Teste 1: Inserir novo pagamento e verificar se o trigger atualiza o status
-- (Use um ID de solicitação aprovada sem pagamento da consulta acima)
INSERT INTO pagamentos (solicitacao_id, valor_pago, data_pagamento, forma_pagamento)
VALUES (3, 320.00, CURRENT_TIMESTAMP, 'PIX');

-- Verificar se o status da solicitação foi atualizado para 'PAGO'
SELECT id, funcionario_id, valor_solicitado, status
FROM solicitacoes
WHERE id = 3;

-- Verificar se foi criado registro no log de auditoria
SELECT *
FROM log_auditoria
WHERE tabela_afetada = 'pagamentos' 
  AND operacao = 'INSERT'
ORDER BY data_operacao DESC
LIMIT 1;

-- Teste 2: Inserir outro pagamento
INSERT INTO pagamentos (solicitacao_id, valor_pago, data_pagamento, forma_pagamento)
VALUES (4, 150.00, CURRENT_TIMESTAMP, 'TED');

-- Verificar resultado
SELECT id, status FROM solicitacoes WHERE id = 4;

-- ============================================================================
-- 3. TESTES DE INTEGRIDADE REFERENCIAL
-- ============================================================================

-- Teste 1: Tentar inserir solicitação com funcionário inexistente (deve falhar)
DO $$
BEGIN
    INSERT INTO solicitacoes (funcionario_id, valor_solicitado, status)
    VALUES (9999, 200.00, 'PENDENTE');
    RAISE NOTICE 'ERRO: Deveria ter falhado - funcionário inexistente';
EXCEPTION
    WHEN foreign_key_violation THEN
        RAISE NOTICE 'SUCESSO: Constraint de foreign key funcionou corretamente';
END $$;

-- Teste 2: Tentar inserir pagamento com solicitação inexistente (deve falhar)
DO $$
BEGIN
    INSERT INTO pagamentos (solicitacao_id, valor_pago, forma_pagamento)
    VALUES (9999, 100.00, 'PIX');
    RAISE NOTICE 'ERRO: Deveria ter falhado - solicitação inexistente';
EXCEPTION
    WHEN foreign_key_violation THEN
        RAISE NOTICE 'SUCESSO: Constraint de foreign key funcionou corretamente';
END $$;

-- Teste 3: Tentar inserir valor negativo (deve falhar)
DO $$
BEGIN
    INSERT INTO solicitacoes (funcionario_id, valor_solicitado, status)
    VALUES (1, -100.00, 'PENDENTE');
    RAISE NOTICE 'ERRO: Deveria ter falhado - valor negativo';
EXCEPTION
    WHEN check_violation THEN
        RAISE NOTICE 'SUCESSO: Constraint CHECK funcionou corretamente';
END $$;

-- ============================================================================
-- 4. TESTES DE UNICIDADE
-- ============================================================================

-- Teste 1: Tentar inserir matrícula duplicada (deve falhar)
DO $$
BEGIN
    INSERT INTO funcionarios (nome, matricula, departamento, data_admissao)
    VALUES ('Teste Duplicado', 'FUNC001', 'TI', CURRENT_DATE);
    RAISE NOTICE 'ERRO: Deveria ter falhado - matrícula duplicada';
EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'SUCESSO: Constraint UNIQUE de matrícula funcionou corretamente';
END $$;

-- Teste 2: Tentar inserir pagamento duplicado para mesma solicitação (deve falhar)
DO $$
BEGIN
    INSERT INTO pagamentos (solicitacao_id, valor_pago, forma_pagamento)
    VALUES (1, 250.00, 'PIX');
    RAISE NOTICE 'ERRO: Deveria ter falhado - pagamento duplicado';
EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'SUCESSO: Constraint UNIQUE de solicitacao_id funcionou corretamente';
END $$;

-- ============================================================================
-- 5. TESTES DAS CONSULTAS
-- ============================================================================

-- Teste da Questão 1: Verificar se retorna apenas aprovados dos últimos 6 meses
SELECT 
    'Questão 1' AS teste,
    COUNT(*) AS registros_retornados,
    MIN(data_solicitacao) AS data_mais_antiga,
    MAX(data_solicitacao) AS data_mais_recente
FROM funcionarios f
INNER JOIN solicitacoes s ON f.id = s.funcionario_id
WHERE s.status = 'APROVADO'
  AND s.data_solicitacao >= CURRENT_DATE - INTERVAL '6 months';

-- Teste da Questão 2: Verificar se há meses com mais de 10 solicitações
SELECT 
    'Questão 2' AS teste,
    TO_CHAR(data_solicitacao, 'YYYY-MM') AS ano_mes,
    COUNT(*) AS total_solicitacoes
FROM solicitacoes
GROUP BY TO_CHAR(data_solicitacao, 'YYYY-MM')
HAVING COUNT(*) > 10;

-- Teste da Questão 5: Verificar quantidade de funcionários por departamento
SELECT 
    'Questão 5' AS teste,
    f.departamento,
    COUNT(DISTINCT f.id) AS funcionarios_com_pagamentos
FROM funcionarios f
INNER JOIN solicitacoes s ON f.id = s.funcionario_id
INNER JOIN pagamentos p ON s.id = p.solicitacao_id
WHERE s.status = 'APROVADO'
GROUP BY f.departamento;

-- ============================================================================
-- 6. RELATÓRIO DE VALIDAÇÃO GERAL
-- ============================================================================

SELECT 
    'Funcionários cadastrados' AS metrica,
    COUNT(*)::TEXT AS valor
FROM funcionarios
UNION ALL
SELECT 
    'Solicitações registradas',
    COUNT(*)::TEXT
FROM solicitacoes
UNION ALL
SELECT 
    'Pagamentos realizados',
    COUNT(*)::TEXT
FROM pagamentos
UNION ALL
SELECT 
    'Logs de auditoria',
    COUNT(*)::TEXT
FROM log_auditoria
UNION ALL
SELECT 
    'Triggers ativos',
    COUNT(*)::TEXT
FROM pg_trigger
WHERE tgrelid = 'pagamentos'::regclass AND tgisinternal = FALSE
UNION ALL
SELECT 
    'Procedures criadas',
    COUNT(*)::TEXT
FROM pg_proc
WHERE proname = 'sp_cancelar_solicitacao';

-- ============================================================================
-- 7. CENÁRIOS ADICIONAIS
-- ============================================================================

-- Cenário 1: Simular aprovação e pagamento de uma solicitação pendente
-- Resetar status se já foi modificado
UPDATE solicitacoes 
SET status = 'APROVADO', observacao = NULL
WHERE id = 23;

-- Verificar resultado
SELECT id, funcionario_id, status FROM solicitacoes WHERE id = 23;

-- Cenário 2: Listar solicitações por status
SELECT 
    status,
    COUNT(*) AS quantidade,
    SUM(valor_solicitado) AS valor_total
FROM solicitacoes
GROUP BY status
ORDER BY quantidade DESC;

-- Cenário 3: Funcionários sem solicitações
SELECT f.id, f.nome, f.departamento
FROM funcionarios f
LEFT JOIN solicitacoes s ON f.id = s.funcionario_id
WHERE s.id IS NULL;

-- ============================================================================
-- FIM DOS TESTES
-- ============================================================================

-- Resumo final
SELECT '============================================' AS resultado;
SELECT 'TESTES CONCLUÍDOS COM SUCESSO!' AS resultado;
SELECT '============================================' AS resultado;
