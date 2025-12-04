-- ============================================================================
-- PROVA DE PROFICIÊNCIA EM BANCO DE DADOS - POSTGRESQL
-- Sistema de Auxílio Transporte
-- Arquivo: 05_questao_03.sql
-- ============================================================================
-- QUESTÃO 3 - TRIGGER (2,0 pontos)
-- ============================================================================
/*
Crie um TRIGGER que:
- Seja acionado APÓS a inserção de um novo registro na tabela pagamentos
- Atualize automaticamente o status da solicitação correspondente para 'PAGO'
- Registre na tabela log_auditoria as informações da operação
*/

-- ============================================================================
-- 1. CRIAR A FUNÇÃO DO TRIGGER
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_atualizar_status_pagamento()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualizar o status da solicitação para 'PAGO'
    UPDATE solicitacoes
    SET status = 'PAGO'
    WHERE id = NEW.solicitacao_id;
    
    -- Registrar a operação no log de auditoria
    INSERT INTO log_auditoria (
        tabela_afetada,
        operacao,
        registro_id,
        detalhes
    ) VALUES (
        'pagamentos',
        'INSERT',
        NEW.id,
        FORMAT(
            'Pagamento realizado - Solicitação ID: %s, Valor: R$ %s, Forma: %s',
            NEW.solicitacao_id,
            NEW.valor_pago,
            NEW.forma_pagamento
        )
    );
    
    -- Retornar o novo registro
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION fn_atualizar_status_pagamento() IS 
'Função trigger que atualiza status da solicitação para PAGO e registra no log de auditoria';

-- ============================================================================
-- 2. CRIAR O TRIGGER
-- ============================================================================

CREATE TRIGGER trg_after_insert_pagamento
    AFTER INSERT ON pagamentos
    FOR EACH ROW
    EXECUTE FUNCTION fn_atualizar_status_pagamento();

COMMENT ON TRIGGER trg_after_insert_pagamento ON pagamentos IS 
'Trigger que executa após inserção de pagamento para atualizar status e auditar';

-- ============================================================================
-- 3. VERIFICAÇÃO
-- ============================================================================

-- Listar triggers da tabela pagamentos
SELECT 
    tgname AS trigger_name,
    tgtype AS trigger_type,
    tgenabled AS enabled
FROM 
    pg_trigger
WHERE 
    tgrelid = 'pagamentos'::regclass
    AND tgisinternal = FALSE;

-- Verificar a função criada
SELECT 
    proname AS function_name,
    prosrc AS function_code
FROM 
    pg_proc
WHERE 
    proname = 'fn_atualizar_status_pagamento';
