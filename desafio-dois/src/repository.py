"""
Camada de persistência de dados usando Repository Pattern
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from threading import Lock

from src.models import Solicitacao, SolicitacaoCreate, SolicitacaoUpdate


class SolicitacaoRepository:
    """Repository para gerenciar persistência de solicitações"""
    
    def __init__(self, data_file: str = "data/solicitacoes.json"):
        """
        Inicializa o repository
        
        Args:
            data_file: Caminho para o arquivo de dados JSON
        """
        self.data_file = Path(data_file)
        self.lock = Lock()  # Thread-safe operations
        self._ensure_data_file()
    
    def _ensure_data_file(self) -> None:
        """Garante que o arquivo de dados existe"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._save_data({"solicitacoes": [], "next_id": 1})
    
    def _load_data(self) -> dict:
        """Carrega dados do arquivo JSON"""
        with self.lock:
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"solicitacoes": [], "next_id": 1}
    
    def _save_data(self, data: dict) -> None:
        """Salva dados no arquivo JSON"""
        with self.lock:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def criar(self, solicitacao_data: SolicitacaoCreate) -> Solicitacao:
        """
        Cria uma nova solicitação
        
        Args:
            solicitacao_data: Dados da solicitação a criar
            
        Returns:
            Solicitação criada com ID atribuído
        """
        data = self._load_data()
        
        # Cria nova solicitação com ID auto-incrementado
        nova_solicitacao = Solicitacao(
            id=data["next_id"],
            tipo=solicitacao_data.tipo,
            descricao=solicitacao_data.descricao,
            status=solicitacao_data.status,
            data_criacao=datetime.now(),
            data_atualizacao=datetime.now()
        )
        
        # Adiciona aos dados
        data["solicitacoes"].append(nova_solicitacao.model_dump(mode='json'))
        data["next_id"] += 1
        
        self._save_data(data)
        return nova_solicitacao
    
    def listar_todas(self) -> List[Solicitacao]:
        """
        Lista todas as solicitações
        
        Returns:
            Lista de todas as solicitações
        """
        data = self._load_data()
        return [Solicitacao(**sol) for sol in data["solicitacoes"]]
    
    def buscar_por_id(self, solicitacao_id: int) -> Optional[Solicitacao]:
        """
        Busca uma solicitação por ID
        
        Args:
            solicitacao_id: ID da solicitação
            
        Returns:
            Solicitação encontrada ou None
        """
        data = self._load_data()
        for sol in data["solicitacoes"]:
            if sol["id"] == solicitacao_id:
                return Solicitacao(**sol)
        return None
    
    def atualizar(self, solicitacao_id: int, solicitacao_update: SolicitacaoUpdate) -> Optional[Solicitacao]:
        """
        Atualiza uma solicitação existente
        
        Args:
            solicitacao_id: ID da solicitação
            solicitacao_update: Dados para atualizar
            
        Returns:
            Solicitação atualizada ou None se não encontrada
        """
        data = self._load_data()
        
        for idx, sol in enumerate(data["solicitacoes"]):
            if sol["id"] == solicitacao_id:
                # Atualiza apenas campos fornecidos
                update_data = solicitacao_update.model_dump(exclude_unset=True)
                sol.update(update_data)
                sol["data_atualizacao"] = datetime.now().isoformat()
                
                data["solicitacoes"][idx] = sol
                self._save_data(data)
                
                return Solicitacao(**sol)
        
        return None
    
    def deletar(self, solicitacao_id: int) -> bool:
        """
        Deleta uma solicitação por ID
        
        Args:
            solicitacao_id: ID da solicitação
            
        Returns:
            True se deletada, False se não encontrada
        """
        data = self._load_data()
        
        solicitacoes_filtradas = [
            sol for sol in data["solicitacoes"] 
            if sol["id"] != solicitacao_id
        ]
        
        if len(solicitacoes_filtradas) == len(data["solicitacoes"]):
            return False  # Nenhuma solicitação foi removida
        
        data["solicitacoes"] = solicitacoes_filtradas
        self._save_data(data)
        return True
    
    def contar(self) -> int:
        """
        Conta o total de solicitações
        
        Returns:
            Número total de solicitações
        """
        data = self._load_data()
        return len(data["solicitacoes"])
