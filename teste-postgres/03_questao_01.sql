-- ============================================================================
-- PROVA DE PROFICIÊNCIA EM BANCO DE DADOS - POSTGRESQL
-- Sistema de Auxílio Transporte
-- Arquivo: 03_questao_01.sql
-- ============================================================================
-- QUESTÃO 1 - JOIN e ORDER BY (2,0 pontos)
-- ============================================================================
/*
Crie uma consulta que retorne:
- Nome do funcionário
- Matrícula
- Departamento
- Valor solicitado
- Status da solicitação
- Data da solicitação

Requisitos:
- Incluir APENAS solicitações com status 'APROVADO'
- Ordenar por departamento (ordem alfabética) e depois por valor solicitado (do maior para o menor)
- Incluir somente solicitações feitas nos últimos 6 meses
*/

SELECT 
    f.nome AS nome_funcionario,
    f.matricula,
    f.departamento,
    s.valor_solicitado,
    s.status,
    s.data_solicitacao
FROM 
    funcionarios f
INNER JOIN 
    solicitacoes s ON f.id = s.funcionario_id
WHERE 
    s.status = 'APROVADO'
    AND s.data_solicitacao >= CURRENT_DATE - INTERVAL '6 months'
ORDER BY 
    f.departamento ASC,
    s.valor_solicitado DESC;

-- ============================================================================
-- ANÁLISE E VALIDAÇÃO
-- ============================================================================

-- Contar registros retornados
SELECT 
    COUNT(*) as total_registros_retornados
FROM 
    funcionarios f
INNER JOIN 
    solicitacoes s ON f.id = s.funcionario_id
WHERE 
    s.status = 'APROVADO'
    AND s.data_solicitacao >= CURRENT_DATE - INTERVAL '6 months';

-- Verificar distribuição por departamento
SELECT 
    f.departamento,
    COUNT(*) as qtd_solicitacoes,
    SUM(s.valor_solicitado) as valor_total,
    AVG(s.valor_solicitado) as valor_medio
FROM 
    funcionarios f
INNER JOIN 
    solicitacoes s ON f.id = s.funcionario_id
WHERE 
    s.status = 'APROVADO'
    AND s.data_solicitacao >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY 
    f.departamento
ORDER BY 
    f.departamento;
