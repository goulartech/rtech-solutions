"""
Testes unitários para o sistema de gerenciamento de solicitações
"""
import pytest
import json
import os
from pathlib import Path
from datetime import datetime

from src.models import (
    Solicitacao,
    SolicitacaoCreate,
    SolicitacaoUpdate,
    StatusSolicitacao,
    TipoSolicitacao
)
from src.repository import SolicitacaoRepository
from src.services import SolicitacaoService


@pytest.fixture
def temp_data_file(tmp_path):
    """Fixture para criar arquivo temporário de dados"""
    data_file = tmp_path / "test_solicitacoes.json"
    return str(data_file)


@pytest.fixture
def repository(temp_data_file):
    """Fixture para criar repository de teste"""
    return SolicitacaoRepository(data_file=temp_data_file)


@pytest.fixture
def service(repository):
    """Fixture para criar service de teste"""
    return SolicitacaoService(repository)


class TestModels:
    """Testes para os modelos Pydantic"""
    
    def test_criar_solicitacao_valida(self):
        """Testa criação de solicitação válida"""
        sol = SolicitacaoCreate(
            tipo=TipoSolicitacao.SUPORTE,
            descricao="Solicitação de teste para verificar o sistema",
            status=StatusSolicitacao.PENDENTE
        )
        assert sol.tipo == TipoSolicitacao.SUPORTE
        assert sol.descricao == "Solicitação de teste para verificar o sistema"
        assert sol.status == StatusSolicitacao.PENDENTE
    
    def test_descricao_muito_curta(self):
        """Testa validação de descrição muito curta"""
        with pytest.raises(ValueError):
            SolicitacaoCreate(
                tipo=TipoSolicitacao.SUPORTE,
                descricao="Curta",
                status=StatusSolicitacao.PENDENTE
            )
    
    def test_descricao_vazia(self):
        """Testa validação de descrição vazia"""
        with pytest.raises(ValueError):
            SolicitacaoCreate(
                tipo=TipoSolicitacao.SUPORTE,
                descricao="          ",
                status=StatusSolicitacao.PENDENTE
            )


class TestRepository:
    """Testes para o Repository"""
    
    def test_criar_solicitacao(self, repository):
        """Testa criação de solicitação no repository"""
        sol_data = SolicitacaoCreate(
            tipo=TipoSolicitacao.MANUTENCAO,
            descricao="Teste de manutenção do sistema principal",
            status=StatusSolicitacao.PENDENTE
        )
        
        sol = repository.criar(sol_data)
        
        assert sol.id == 1
        assert sol.tipo == TipoSolicitacao.MANUTENCAO
        assert sol.descricao == "Teste de manutenção do sistema principal"
        assert sol.status == StatusSolicitacao.PENDENTE
    
    def test_listar_solicitacoes_vazio(self, repository):
        """Testa listagem quando não há solicitações"""
        solicitacoes = repository.listar_todas()
        assert len(solicitacoes) == 0
    
    def test_listar_solicitacoes(self, repository):
        """Testa listagem de solicitações"""
        # Cria 3 solicitações
        for i in range(3):
            sol_data = SolicitacaoCreate(
                tipo=TipoSolicitacao.SUPORTE,
                descricao=f"Solicitação de teste número {i+1} para o sistema",
                status=StatusSolicitacao.PENDENTE
            )
            repository.criar(sol_data)
        
        solicitacoes = repository.listar_todas()
        assert len(solicitacoes) == 3
    
    def test_buscar_por_id_existente(self, repository):
        """Testa busca de solicitação existente"""
        sol_data = SolicitacaoCreate(
            tipo=TipoSolicitacao.DESENVOLVIMENTO,
            descricao="Desenvolvimento de nova funcionalidade no módulo X",
            status=StatusSolicitacao.PENDENTE
        )
        sol_criada = repository.criar(sol_data)
        
        sol_encontrada = repository.buscar_por_id(sol_criada.id)
        assert sol_encontrada is not None
        assert sol_encontrada.id == sol_criada.id
    
    def test_buscar_por_id_inexistente(self, repository):
        """Testa busca de solicitação inexistente"""
        sol = repository.buscar_por_id(999)
        assert sol is None
    
    def test_atualizar_solicitacao(self, repository):
        """Testa atualização de solicitação"""
        sol_data = SolicitacaoCreate(
            tipo=TipoSolicitacao.CONSULTA,
            descricao="Consulta sobre funcionamento do sistema principal",
            status=StatusSolicitacao.PENDENTE
        )
        sol_criada = repository.criar(sol_data)
        
        update_data = SolicitacaoUpdate(
            status=StatusSolicitacao.EM_ANDAMENTO
        )
        sol_atualizada = repository.atualizar(sol_criada.id, update_data)
        
        assert sol_atualizada is not None
        assert sol_atualizada.status == StatusSolicitacao.EM_ANDAMENTO
    
    def test_deletar_solicitacao(self, repository):
        """Testa deleção de solicitação"""
        sol_data = SolicitacaoCreate(
            tipo=TipoSolicitacao.OUTROS,
            descricao="Solicitação que será deletada para teste do sistema",
            status=StatusSolicitacao.PENDENTE
        )
        sol_criada = repository.criar(sol_data)
        
        success = repository.deletar(sol_criada.id)
        assert success is True
        
        sol_deletada = repository.buscar_por_id(sol_criada.id)
        assert sol_deletada is None
    
    def test_deletar_solicitacao_inexistente(self, repository):
        """Testa deleção de solicitação inexistente"""
        success = repository.deletar(999)
        assert success is False
    
    def test_contar_solicitacoes(self, repository):
        """Testa contagem de solicitações"""
        assert repository.contar() == 0
        
        for i in range(5):
            sol_data = SolicitacaoCreate(
                tipo=TipoSolicitacao.SUPORTE,
                descricao=f"Solicitação número {i+1} para contagem de teste",
                status=StatusSolicitacao.PENDENTE
            )
            repository.criar(sol_data)
        
        assert repository.contar() == 5


class TestService:
    """Testes para o Service"""
    
    def test_criar_solicitacao(self, service):
        """Testa criação via service"""
        sol_data = SolicitacaoCreate(
            tipo=TipoSolicitacao.MANUTENCAO,
            descricao="Manutenção preventiva do sistema de banco de dados",
            status=StatusSolicitacao.PENDENTE
        )
        
        sol = service.criar_solicitacao(sol_data)
        assert sol.id == 1
    
    def test_listar_solicitacoes_ordenadas(self, service):
        """Testa listagem ordenada por data"""
        for i in range(3):
            sol_data = SolicitacaoCreate(
                tipo=TipoSolicitacao.SUPORTE,
                descricao=f"Solicitação {i+1} para teste de ordenação cronológica",
                status=StatusSolicitacao.PENDENTE
            )
            service.criar_solicitacao(sol_data)
        
        solicitacoes = service.listar_solicitacoes()
        assert len(solicitacoes) == 3
        # Verifica ordenação reversa (mais recente primeiro)
        assert solicitacoes[0].id > solicitacoes[1].id
    
    def test_listar_por_status(self, service):
        """Testa filtro por status"""
        # Cria solicitações com diferentes status
        sol1 = SolicitacaoCreate(
            tipo=TipoSolicitacao.SUPORTE,
            descricao="Primeira solicitação com status pendente para filtro",
            status=StatusSolicitacao.PENDENTE
        )
        sol2 = SolicitacaoCreate(
            tipo=TipoSolicitacao.SUPORTE,
            descricao="Segunda solicitação com status em andamento para filtro",
            status=StatusSolicitacao.EM_ANDAMENTO
        )
        
        service.criar_solicitacao(sol1)
        service.criar_solicitacao(sol2)
        
        pendentes = service.listar_solicitacoes(status=StatusSolicitacao.PENDENTE)
        assert len(pendentes) == 1
        assert pendentes[0].status == StatusSolicitacao.PENDENTE
    
    def test_atualizar_status(self, service):
        """Testa atualização de status via service"""
        sol_data = SolicitacaoCreate(
            tipo=TipoSolicitacao.DESENVOLVIMENTO,
            descricao="Desenvolvimento que terá seu status atualizado",
            status=StatusSolicitacao.PENDENTE
        )
        sol = service.criar_solicitacao(sol_data)
        
        sol_atualizada = service.atualizar_status(sol.id, StatusSolicitacao.CONCLUIDA)
        assert sol_atualizada.status == StatusSolicitacao.CONCLUIDA
    
    def test_obter_estatisticas(self, service):
        """Testa geração de estatísticas"""
        # Cria solicitações variadas
        sol1 = SolicitacaoCreate(
            tipo=TipoSolicitacao.SUPORTE,
            descricao="Suporte técnico para estatísticas de teste",
            status=StatusSolicitacao.PENDENTE
        )
        sol2 = SolicitacaoCreate(
            tipo=TipoSolicitacao.SUPORTE,
            descricao="Outro suporte técnico para estatísticas",
            status=StatusSolicitacao.EM_ANDAMENTO
        )
        sol3 = SolicitacaoCreate(
            tipo=TipoSolicitacao.MANUTENCAO,
            descricao="Manutenção para teste de estatísticas",
            status=StatusSolicitacao.PENDENTE
        )
        
        service.criar_solicitacao(sol1)
        service.criar_solicitacao(sol2)
        service.criar_solicitacao(sol3)
        
        stats = service.obter_estatisticas()
        
        assert stats["total"] == 3
        assert stats["por_status"]["pendente"] == 2
        assert stats["por_status"]["em_andamento"] == 1
        assert stats["por_tipo"]["suporte"] == 2
        assert stats["por_tipo"]["manutencao"] == 1


class TestAPI:
    """Testes para a API (testes de integração básicos)"""
    
    @pytest.fixture
    def client(self):
        """Fixture para cliente de teste da API"""
        from fastapi.testclient import TestClient
        
        # Reconfigura a aplicação para usar repositório de teste
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        
        from app import app
        from src.repository import SolicitacaoRepository
        from src.services import SolicitacaoService
        
        # Substitui dependências por versões de teste
        test_repository = SolicitacaoRepository(data_file=temp_file.name)
        test_service = SolicitacaoService(test_repository)
        
        # Injetar dependências de teste na app
        app.state.repository = test_repository
        app.state.service = test_service
        
        client = TestClient(app)
        yield client
        
        # Cleanup
        os.unlink(temp_file.name)
    
    def test_health_check(self, client):
        """Testa endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_criar_solicitacao_api(self, client):
        """Testa criação via API"""
        payload = {
            "tipo": "suporte",
            "descricao": "Teste de criação via API do sistema",
            "status": "pendente"
        }
        
        response = client.post("/solicitacoes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["tipo"] == "suporte"
        assert "id" in data
    
    def test_listar_solicitacoes_api(self, client):
        """Testa listagem via API"""
        # Primeiro cria uma solicitação
        payload = {
            "tipo": "manutencao",
            "descricao": "Teste de listagem via API do sistema",
            "status": "pendente"
        }
        client.post("/solicitacoes", json=payload)
        
        # Lista todas
        response = client.get("/solicitacoes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_obter_solicitacao_por_id(self, client):
        """Testa obtenção de solicitação específica"""
        # Cria uma solicitação
        payload = {
            "tipo": "consulta",
            "descricao": "Teste de busca por ID via API do sistema",
            "status": "pendente"
        }
        create_response = client.post("/solicitacoes", json=payload)
        sol_id = create_response.json()["id"]
        
        # Busca por ID
        response = client.get(f"/solicitacoes/{sol_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sol_id
    
    def test_atualizar_solicitacao_api(self, client):
        """Testa atualização via API"""
        # Cria uma solicitação
        payload = {
            "tipo": "outros",
            "descricao": "Teste de atualização via API do sistema",
            "status": "pendente"
        }
        create_response = client.post("/solicitacoes", json=payload)
        sol_id = create_response.json()["id"]
        
        # Atualiza
        update_payload = {
            "status": "concluida"
        }
        response = client.put(f"/solicitacoes/{sol_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "concluida"
    
    def test_deletar_solicitacao_api(self, client):
        """Testa deleção via API"""
        # Cria uma solicitação
        payload = {
            "tipo": "desenvolvimento",
            "descricao": "Teste de deleção via API do sistema",
            "status": "pendente"
        }
        create_response = client.post("/solicitacoes", json=payload)
        sol_id = create_response.json()["id"]
        
        # Deleta
        response = client.delete(f"/solicitacoes/{sol_id}")
        assert response.status_code == 204
        
        # Verifica que foi deletada
        get_response = client.get(f"/solicitacoes/{sol_id}")
        assert get_response.status_code == 404
