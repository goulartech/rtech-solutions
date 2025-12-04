"""
API REST com FastAPI para gerenciamento de solicitações
"""
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from src.models import (
    Solicitacao, 
    SolicitacaoCreate, 
    SolicitacaoUpdate, 
    StatusSolicitacao
)
from src.repository import SolicitacaoRepository
from src.services import SolicitacaoService


# Inicializa aplicação
app = FastAPI(
    title="Sistema de Gerenciamento de Solicitações",
    description="API REST completa para gerenciar solicitações com operações CRUD",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS para permitir acesso do Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa dependências
repository = SolicitacaoRepository()
service = SolicitacaoService(repository)


@app.get("/", tags=["Health"])
async def root():
    """Endpoint raiz para verificar se a API está funcionando"""
    return {
        "message": "API de Gerenciamento de Solicitações",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Verifica o status da aplicação"""
    total = repository.contar()
    return {
        "status": "healthy",
        "total_solicitacoes": total
    }


@app.post(
    "/solicitacoes",
    response_model=Solicitacao,
    status_code=status.HTTP_201_CREATED,
    tags=["Solicitações"]
)
async def criar_solicitacao(solicitacao: SolicitacaoCreate):
    """
    Cria uma nova solicitação
    
    - **tipo**: Tipo da solicitação (manutencao, suporte, desenvolvimento, consulta, outros)
    - **descricao**: Descrição detalhada (10-500 caracteres)
    - **status**: Status inicial (padrão: pendente)
    """
    try:
        return service.criar_solicitacao(solicitacao)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar solicitação: {str(e)}"
        )


@app.get(
    "/solicitacoes",
    response_model=List[Solicitacao],
    tags=["Solicitações"]
)
async def listar_solicitacoes(
    status_filter: Optional[StatusSolicitacao] = Query(
        None, 
        description="Filtrar por status",
        alias="status"
    )
):
    """
    Lista todas as solicitações
    
    - **status**: Filtro opcional por status
    """
    try:
        return service.listar_solicitacoes(status=status_filter)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar solicitações: {str(e)}"
        )


@app.get(
    "/solicitacoes/{solicitacao_id}",
    response_model=Solicitacao,
    tags=["Solicitações"]
)
async def obter_solicitacao(solicitacao_id: int):
    """
    Obtém uma solicitação específica por ID
    
    - **solicitacao_id**: ID da solicitação
    """
    solicitacao = service.obter_solicitacao(solicitacao_id)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solicitação com ID {solicitacao_id} não encontrada"
        )
    return solicitacao


@app.put(
    "/solicitacoes/{solicitacao_id}",
    response_model=Solicitacao,
    tags=["Solicitações"]
)
async def atualizar_solicitacao(
    solicitacao_id: int,
    solicitacao_update: SolicitacaoUpdate
):
    """
    Atualiza uma solicitação existente
    
    - **solicitacao_id**: ID da solicitação
    - **tipo**: Novo tipo (opcional)
    - **descricao**: Nova descrição (opcional)
    - **status**: Novo status (opcional)
    """
    solicitacao = service.atualizar_solicitacao(solicitacao_id, solicitacao_update)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solicitação com ID {solicitacao_id} não encontrada"
        )
    return solicitacao


@app.patch(
    "/solicitacoes/{solicitacao_id}/status",
    response_model=Solicitacao,
    tags=["Solicitações"]
)
async def atualizar_status(
    solicitacao_id: int,
    novo_status: StatusSolicitacao
):
    """
    Atualiza apenas o status de uma solicitação
    
    - **solicitacao_id**: ID da solicitação
    - **novo_status**: Novo status a ser aplicado
    """
    solicitacao = service.atualizar_status(solicitacao_id, novo_status)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solicitação com ID {solicitacao_id} não encontrada"
        )
    return solicitacao


@app.delete(
    "/solicitacoes/{solicitacao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Solicitações"]
)
async def deletar_solicitacao(solicitacao_id: int):
    """
    Deleta uma solicitação pelo ID
    
    - **solicitacao_id**: ID da solicitação a ser deletada
    """
    success = service.deletar_solicitacao(solicitacao_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solicitação com ID {solicitacao_id} não encontrada"
        )


@app.get(
    "/solicitacoes/estatisticas/geral",
    tags=["Estatísticas"]
)
async def obter_estatisticas():
    """
    Obtém estatísticas gerais sobre as solicitações
    
    Retorna contagens por status e por tipo
    """
    try:
        return service.obter_estatisticas()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter estatísticas: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
