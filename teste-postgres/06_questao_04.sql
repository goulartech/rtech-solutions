-- ============================================================================
-- PROVA DE PROFICIÊNCIA EM BANCO DE DADOS - POSTGRESQL
-- Sistema de Auxílio Transporte
-- Arquivo: 06_questao_04.sql
-- ============================================================================
-- QUESTÃO 4 - STORED PROCEDURE (2,0 pontos)
-- ============================================================================
/*
Crie uma STORED PROCEDURE chamada sp_cancelar_solicitacao que:
- Receba ID da solicitação e motivo
- Verifique se pode cancelar (não pode se já foi PAGO)
- Atualize o status para CANCELADO
- Registre no log
- Retorne mensagem de sucesso ou erro
*/

-- ============================================================================
-- CRIAR A STORED PROCEDURE
-- ============================================================================

CREATE OR REPLACE FUNCTION sp_cancelar_solicitacao(
    p_solicitacao_id INTEGER,
    p_motivo TEXT
) 
RETURNS TEXT AS $$
DECLARE
    v_status_atual VARCHAR(20);
    v_funcionario_id INTEGER;
    v_valor_solicitado NUMERIC(10,2);
BEGIN
    -- Verificar se a solicitação existe e obter o status atual
    SELECT status, funcionario_id, valor_solicitado
    INTO v_status_atual, v_funcionario_id, v_valor_solicitado
    FROM solicitacoes
    WHERE id = p_solicitacao_id;
    
    -- Validar se a solicitação existe
    IF NOT FOUND THEN
        RETURN FORMAT('ERRO: Solicitação ID %s não encontrada.', p_solicitacao_id);
    END IF;
    
    -- Validar se a solicitação já foi paga
    IF v_status_atual = 'PAGO' THEN
        RETURN FORMAT(
            'ERRO: Não é possível cancelar a solicitação ID %s. Status atual: %s. Solicitações pagas não podem ser canceladas.',
            p_solicitacao_id,
            v_status_atual
        );
    END IF;
    
    -- Validar se a solicitação já está cancelada
    IF v_status_atual = 'CANCELADO' THEN
        RETURN FORMAT(
            'AVISO: A solicitação ID %s já está cancelada.',
            p_solicitacao_id
        );
    END IF;
    
    -- Atualizar o status para CANCELADO
    UPDATE solicitacoes
    SET status = 'CANCELADO',
        observacao = COALESCE(observacao || ' | ', '') || 'CANCELADO: ' || p_motivo
    WHERE id = p_solicitacao_id;
    
    -- Registrar no log de auditoria
    INSERT INTO log_auditoria (
        tabela_afetada,
        operacao,
        registro_id,
        detalhes
    ) VALUES (
        'solicitacoes',
        'UPDATE',
        p_solicitacao_id,
        FORMAT(
            'Solicitação cancelada - Funcionário ID: %s, Valor: R$ %s, Motivo: %s',
            v_funcionario_id,
            v_valor_solicitado,
            p_motivo
        )
    );
    
    -- Retornar mensagem de sucesso
    RETURN FORMAT(
        'SUCESSO: Solicitação ID %s cancelada com sucesso. Motivo: %s',
        p_solicitacao_id,
        p_motivo
    );
    
EXCEPTION
    WHEN OTHERS THEN
        -- Capturar qualquer erro não tratado
        RETURN FORMAT(
            'ERRO: Falha ao cancelar solicitação ID %s. Detalhes: %s',
            p_solicitacao_id,
            SQLERRM
        );
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION sp_cancelar_solicitacao(INTEGER, TEXT) IS 
'Procedure para cancelar solicitações com validações de regras de negócio e auditoria';

-- ============================================================================
-- VERIFICAÇÃO
-- ============================================================================

-- Verificar se a procedure foi criada
SELECT 
    proname AS procedure_name,
    pg_get_function_arguments(oid) AS arguments,
    pg_get_functiondef(oid) AS definition
FROM 
    pg_proc
WHERE 
    proname = 'sp_cancelar_solicitacao';
