-- ============================================================================
-- PROVA DE PROFICIÊNCIA EM BANCO DE DADOS - POSTGRESQL
-- Sistema de Auxílio Transporte
-- Arquivo: 04_questao_02.sql
-- ============================================================================
-- QUESTÃO 2 - GROUP BY e HAVING (2,0 pontos)
-- ============================================================================
/*
Crie uma consulta que mostre um relatório mensal de solicitações, contendo:
- Ano e mês da solicitação
- Quantidade total de solicitações
- Valor total solicitado
- Valor médio das solicitações
- Quantidade de solicitações aprovadas

Requisitos:
- Agrupar por ano e mês
- Mostrar APENAS os meses que tiveram mais de 10 solicitações
- Ordenar do mês mais recente para o mais antigo
- Formatar o ano/mês como 'YYYY-MM'
*/

SELECT 
    TO_CHAR(data_solicitacao, 'YYYY-MM') AS ano_mes,
    COUNT(*) AS total_solicitacoes,
    SUM(valor_solicitado) AS valor_total,
    ROUND(AVG(valor_solicitado), 2) AS valor_medio,
    COUNT(*) FILTER (WHERE status = 'APROVADO') AS qtd_aprovadas
FROM 
    solicitacoes
GROUP BY 
    TO_CHAR(data_solicitacao, 'YYYY-MM'),
    DATE_TRUNC('month', data_solicitacao)
HAVING 
    COUNT(*) > 10
ORDER BY 
    DATE_TRUNC('month', data_solicitacao) DESC;

-- ============================================================================
-- ANÁLISE E VALIDAÇÃO
-- ============================================================================

-- Verificar total de solicitações por mês (sem filtro HAVING)
SELECT 
    TO_CHAR(data_solicitacao, 'YYYY-MM') AS ano_mes,
    COUNT(*) AS total_solicitacoes
FROM 
    solicitacoes
GROUP BY 
    TO_CHAR(data_solicitacao, 'YYYY-MM'),
    DATE_TRUNC('month', data_solicitacao)
ORDER BY 
    DATE_TRUNC('month', data_solicitacao) DESC;

-- ============================================================================
-- OBSERVAÇÃO IMPORTANTE
-- ============================================================================
/*
Com os dados atuais (25 registros distribuídos ao longo de vários meses),
é possível que nenhum mês tenha mais de 10 solicitações.

Caso a consulta principal não retorne resultados, ajustar os dados em
02_insert_data.sql concentrando mais solicitações em um único mês.

Sugestão: Adicionar mais registros para novembro/2025 para atingir o requisito.
*/

-- Script auxiliar para adicionar mais solicitações em novembro/2025
-- (Comentado - descomentar se necessário para atender ao requisito)

/*
INSERT INTO solicitacoes (funcionario_id, valor_solicitado, data_solicitacao, status, observacao) VALUES
(1, 200.00, '2025-11-05 10:00:00', 'APROVADO', 'Transporte adicional'),
(2, 180.00, '2025-11-06 11:00:00', 'APROVADO', 'Deslocamento extra'),
(3, 220.00, '2025-11-07 12:00:00', 'APROVADO', 'Reunião externa'),
(4, 190.00, '2025-11-08 13:00:00', 'PENDENTE', 'Solicitação em análise'),
(5, 210.00, '2025-11-09 14:00:00', 'APROVADO', 'Visita cliente');
*/
