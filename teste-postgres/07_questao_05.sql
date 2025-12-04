-- ============================================================================
-- PROVA DE PROFICIÊNCIA EM BANCO DE DADOS - POSTGRESQL
-- Sistema de Auxílio Transporte
-- Arquivo: 07_questao_05.sql
-- ============================================================================
-- QUESTÃO 5 - SUBCONSULTA e WINDOW FUNCTION (2,0 pontos)
-- ============================================================================
/*
Crie uma consulta que identifique os funcionários "top gastadores":
- Nome do funcionário
- Departamento
- Total gasto
- Quantidade de solicitações aprovadas
- Ranking dentro do departamento
- Percentual do total do departamento

Requisitos:
- Apenas solicitações APROVADAS com pagamentos
- TOP 3 de cada departamento
- Percentual com 2 casas decimais
*/

-- ============================================================================
-- SOLUÇÃO COM CTE E WINDOW FUNCTIONS
-- ============================================================================

WITH gastos_por_funcionario AS (
    -- Calcular o total gasto por funcionário (apenas solicitações aprovadas com pagamento)
    SELECT 
        f.id AS funcionario_id,
        f.nome,
        f.departamento,
        SUM(s.valor_solicitado) AS total_gasto,
        COUNT(s.id) AS qtd_solicitacoes
    FROM 
        funcionarios f
    INNER JOIN 
        solicitacoes s ON f.id = s.funcionario_id
    INNER JOIN 
        pagamentos p ON s.id = p.solicitacao_id
    WHERE 
        s.status = 'APROVADO'
    GROUP BY 
        f.id, f.nome, f.departamento
),
total_por_departamento AS (
    -- Calcular o total gasto por departamento
    SELECT 
        departamento,
        SUM(total_gasto) AS total_departamento
    FROM 
        gastos_por_funcionario
    GROUP BY 
        departamento
),
ranking_funcionarios AS (
    -- Calcular o ranking dentro de cada departamento
    SELECT 
        gf.funcionario_id,
        gf.nome,
        gf.departamento,
        gf.total_gasto,
        gf.qtd_solicitacoes,
        ROW_NUMBER() OVER (
            PARTITION BY gf.departamento 
            ORDER BY gf.total_gasto DESC
        ) AS ranking,
        td.total_departamento
    FROM 
        gastos_por_funcionario gf
    INNER JOIN 
        total_por_departamento td ON gf.departamento = td.departamento
)
-- Selecionar apenas o TOP 3 de cada departamento
SELECT 
    nome AS nome_funcionario,
    departamento,
    total_gasto,
    qtd_solicitacoes AS qtd_solicitacoes_aprovadas,
    ranking AS ranking_departamento,
    ROUND((total_gasto / total_departamento * 100), 2) AS percentual_departamento
FROM 
    ranking_funcionarios
WHERE 
    ranking <= 3
ORDER BY 
    departamento ASC,
    ranking ASC;

-- ============================================================================
-- ANÁLISE E VALIDAÇÃO
-- ============================================================================

-- Verificar total de funcionários com pagamentos por departamento
SELECT 
    f.departamento,
    COUNT(DISTINCT f.id) AS qtd_funcionarios_com_pagamentos
FROM 
    funcionarios f
INNER JOIN 
    solicitacoes s ON f.id = s.funcionario_id
INNER JOIN 
    pagamentos p ON s.id = p.solicitacao_id
WHERE 
    s.status = 'APROVADO'
GROUP BY 
    f.departamento
ORDER BY 
    f.departamento;

-- Verificar total gasto por departamento
SELECT 
    f.departamento,
    COUNT(DISTINCT f.id) AS qtd_funcionarios,
    SUM(s.valor_solicitado) AS total_departamento,
    AVG(s.valor_solicitado) AS media_por_solicitacao
FROM 
    funcionarios f
INNER JOIN 
    solicitacoes s ON f.id = s.funcionario_id
INNER JOIN 
    pagamentos p ON s.id = p.solicitacao_id
WHERE 
    s.status = 'APROVADO'
GROUP BY 
    f.departamento
ORDER BY 
    total_departamento DESC;

-- Verificar se a soma dos percentuais está correta
WITH gastos_por_funcionario AS (
    SELECT 
        f.id AS funcionario_id,
        f.nome,
        f.departamento,
        SUM(s.valor_solicitado) AS total_gasto,
        COUNT(s.id) AS qtd_solicitacoes
    FROM 
        funcionarios f
    INNER JOIN 
        solicitacoes s ON f.id = s.funcionario_id
    INNER JOIN 
        pagamentos p ON s.id = p.solicitacao_id
    WHERE 
        s.status = 'APROVADO'
    GROUP BY 
        f.id, f.nome, f.departamento
),
total_por_departamento AS (
    SELECT 
        departamento,
        SUM(total_gasto) AS total_departamento
    FROM 
        gastos_por_funcionario
    GROUP BY 
        departamento
),
ranking_funcionarios AS (
    SELECT 
        gf.funcionario_id,
        gf.nome,
        gf.departamento,
        gf.total_gasto,
        gf.qtd_solicitacoes,
        ROW_NUMBER() OVER (
            PARTITION BY gf.departamento 
            ORDER BY gf.total_gasto DESC
        ) AS ranking,
        td.total_departamento
    FROM 
        gastos_por_funcionario gf
    INNER JOIN 
        total_por_departamento td ON gf.departamento = td.departamento
)
SELECT 
    departamento,
    SUM(ROUND((total_gasto / total_departamento * 100), 2)) AS soma_percentuais_top3
FROM 
    ranking_funcionarios
WHERE 
    ranking <= 3
GROUP BY 
    departamento
ORDER BY 
    departamento;
