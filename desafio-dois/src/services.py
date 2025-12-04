"""
Camada de serviços com lógica de negócio
"""
from typing import List, Optional

from src.models import Solicitacao, SolicitacaoCreate, SolicitacaoUpdate, StatusSolicitacao
from src.repository import SolicitacaoRepository


class SolicitacaoService:
    """Serviço para gerenciar lógica de negócio de solicitações"""
    
    def __init__(self, repository: SolicitacaoRepository):
        """
        Inicializa o serviço
        
        Args:
            repository: Repository de solicitações
        """
        self.repository = repository
    
    def criar_solicitacao(self, solicitacao_data: SolicitacaoCreate) -> Solicitacao:
        """
        Cria uma nova solicitação
        
        Args:
            solicitacao_data: Dados da solicitação
            
        Returns:
            Solicitação criada
        """
        return self.repository.criar(solicitacao_data)
    
    def listar_solicitacoes(self, status: Optional[StatusSolicitacao] = None) -> List[Solicitacao]:
        """
        Lista todas as solicitações, opcionalmente filtradas por status
        
        Args:
            status: Status para filtrar (opcional)
            
        Returns:
            Lista de solicitações
        """
        solicitacoes = self.repository.listar_todas()
        
        if status:
            solicitacoes = [s for s in solicitacoes if s.status == status]
        
        return sorted(solicitacoes, key=lambda x: x.data_criacao, reverse=True)
    
    def obter_solicitacao(self, solicitacao_id: int) -> Optional[Solicitacao]:
        """
        Obtém uma solicitação por ID
        
        Args:
            solicitacao_id: ID da solicitação
            
        Returns:
            Solicitação encontrada ou None
        """
        return self.repository.buscar_por_id(solicitacao_id)
    
    def atualizar_solicitacao(
        self, 
        solicitacao_id: int, 
        solicitacao_update: SolicitacaoUpdate
    ) -> Optional[Solicitacao]:
        """
        Atualiza uma solicitação existente
        
        Args:
            solicitacao_id: ID da solicitação
            solicitacao_update: Dados para atualizar
            
        Returns:
            Solicitação atualizada ou None se não encontrada
        """
        return self.repository.atualizar(solicitacao_id, solicitacao_update)
    
    def atualizar_status(
        self, 
        solicitacao_id: int, 
        novo_status: StatusSolicitacao
    ) -> Optional[Solicitacao]:
        """
        Atualiza apenas o status de uma solicitação
        
        Args:
            solicitacao_id: ID da solicitação
            novo_status: Novo status
            
        Returns:
            Solicitação atualizada ou None se não encontrada
        """
        update_data = SolicitacaoUpdate(status=novo_status)
        return self.repository.atualizar(solicitacao_id, update_data)
    
    def deletar_solicitacao(self, solicitacao_id: int) -> bool:
        """
        Deleta uma solicitação
        
        Args:
            solicitacao_id: ID da solicitação
            
        Returns:
            True se deletada com sucesso, False caso contrário
        """
        return self.repository.deletar(solicitacao_id)
    
    def obter_estatisticas(self) -> dict:
        """
        Obtém estatísticas sobre as solicitações
        
        Returns:
            Dicionário com estatísticas
        """
        solicitacoes = self.repository.listar_todas()
        
        stats = {
            "total": len(solicitacoes),
            "por_status": {},
            "por_tipo": {}
        }
        
        for sol in solicitacoes:
            # Contagem por status
            status_key = sol.status.value
            stats["por_status"][status_key] = stats["por_status"].get(status_key, 0) + 1
            
            # Contagem por tipo
            tipo_key = sol.tipo.value
            stats["por_tipo"][tipo_key] = stats["por_tipo"].get(tipo_key, 0) + 1
        
        return stats
