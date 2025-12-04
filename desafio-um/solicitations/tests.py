"""
Testes para a app solicitations
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from decimal import Decimal

from .models import Request


class RequestModelTest(TestCase):
    """Testes para o modelo Request"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.valid_ferias_data = {
            'tipo': Request.TIPO_FERIAS,
            'titulo': 'Férias de Verão',
            'descricao': 'Férias programadas para janeiro',
            'solicitante': 'João Silva',
            'data_inicio': date.today() + timedelta(days=30),
            'data_fim': date.today() + timedelta(days=44),
        }
        
        self.valid_reembolso_data = {
            'tipo': Request.TIPO_REEMBOLSO,
            'titulo': 'Reembolso de Transporte',
            'descricao': 'Despesas com transporte do projeto X',
            'solicitante': 'Maria Santos',
            'valor': Decimal('150.00'),
        }
    
    def test_criar_solicitacao_ferias_valida(self):
        """Testa criação de solicitação de férias válida"""
        solicitacao = Request.objects.create(**self.valid_ferias_data)
        self.assertEqual(solicitacao.tipo, Request.TIPO_FERIAS)
        self.assertEqual(solicitacao.status, Request.STATUS_PENDENTE)
        self.assertIsNotNone(solicitacao.duracao_dias)
        self.assertEqual(solicitacao.duracao_dias, 15)
    
    def test_criar_solicitacao_reembolso_valida(self):
        """Testa criação de solicitação de reembolso válida"""
        solicitacao = Request.objects.create(**self.valid_reembolso_data)
        self.assertEqual(solicitacao.tipo, Request.TIPO_REEMBOLSO)
        self.assertEqual(solicitacao.valor, Decimal('150.00'))
    
    def test_ferias_sem_data_inicio_invalida(self):
        """Testa que férias sem data de início é inválida"""
        data = self.valid_ferias_data.copy()
        data.pop('data_inicio')
        
        with self.assertRaises(ValidationError):
            Request.objects.create(**data)
    
    def test_reembolso_sem_valor_invalido(self):
        """Testa que reembolso sem valor é inválido"""
        data = self.valid_reembolso_data.copy()
        data.pop('valor')
        
        with self.assertRaises(ValidationError):
            Request.objects.create(**data)
    
    def test_data_fim_antes_data_inicio_invalida(self):
        """Testa que data de término antes da data de início é inválida"""
        data = self.valid_ferias_data.copy()
        data['data_fim'] = data['data_inicio'] - timedelta(days=1)
        
        with self.assertRaises(ValidationError):
            Request.objects.create(**data)
    
    def test_aprovar_solicitacao(self):
        """Testa aprovação de solicitação"""
        solicitacao = Request.objects.create(**self.valid_ferias_data)
        solicitacao.aprovar('Aprovado pela gerência')
        
        self.assertEqual(solicitacao.status, Request.STATUS_APROVADO)
        self.assertEqual(solicitacao.observacoes, 'Aprovado pela gerência')
    
    def test_rejeitar_solicitacao(self):
        """Testa rejeição de solicitação"""
        solicitacao = Request.objects.create(**self.valid_ferias_data)
        solicitacao.rejeitar('Fora do período permitido')
        
        self.assertEqual(solicitacao.status, Request.STATUS_REJEITADO)
        self.assertEqual(solicitacao.observacoes, 'Fora do período permitido')
    
    def test_cancelar_solicitacao(self):
        """Testa cancelamento de solicitação"""
        solicitacao = Request.objects.create(**self.valid_ferias_data)
        solicitacao.cancelar('Cancelado pelo solicitante')
        
        self.assertEqual(solicitacao.status, Request.STATUS_CANCELADO)
    
    def test_nao_pode_aprovar_solicitacao_aprovada(self):
        """Testa que não pode aprovar solicitação já aprovada"""
        solicitacao = Request.objects.create(**self.valid_ferias_data)
        solicitacao.aprovar()
        
        with self.assertRaises(ValueError):
            solicitacao.aprovar()
    
    def test_nao_pode_cancelar_solicitacao_aprovada(self):
        """Testa que não pode cancelar solicitação aprovada"""
        solicitacao = Request.objects.create(**self.valid_ferias_data)
        solicitacao.aprovar()
        
        with self.assertRaises(ValueError):
            solicitacao.cancelar()


class RequestAPITest(APITestCase):
    """Testes para a API de solicitações"""
    
    def setUp(self):
        """Configuração inicial para os testes da API"""
        self.list_url = '/api/v1/solicitacoes/'
        self.valid_ferias_payload = {
            'tipo': 'ferias',
            'titulo': 'Férias de Fim de Ano',
            'descricao': 'Férias programadas para dezembro',
            'solicitante': 'Carlos Souza',
            'data_inicio': str(date.today() + timedelta(days=60)),
            'data_fim': str(date.today() + timedelta(days=74)),
        }
        
        self.valid_reembolso_payload = {
            'tipo': 'reembolso',
            'titulo': 'Reembolso de Alimentação',
            'descricao': 'Despesas com alimentação em viagem',
            'solicitante': 'Ana Costa',
            'valor': '250.00',
        }
    
    def test_listar_solicitacoes(self):
        """Testa listagem de solicitações"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_criar_solicitacao_ferias(self):
        """Testa criação de solicitação de férias via API"""
        response = self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tipo'], 'ferias')
        self.assertIn('id', response.data)
    
    def test_criar_solicitacao_reembolso(self):
        """Testa criação de solicitação de reembolso via API"""
        response = self.client.post(self.list_url, self.valid_reembolso_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tipo'], 'reembolso')
    
    def test_criar_solicitacao_ferias_sem_data_inicio(self):
        """Testa que não é possível criar férias sem data de início"""
        payload = self.valid_ferias_payload.copy()
        payload.pop('data_inicio')
        
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_inicio', response.data)
    
    def test_criar_solicitacao_reembolso_sem_valor(self):
        """Testa que não é possível criar reembolso sem valor"""
        payload = self.valid_reembolso_payload.copy()
        payload.pop('valor')
        
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('valor', response.data)
    
    def test_visualizar_detalhes_solicitacao(self):
        """Testa visualização de detalhes de uma solicitação"""
        response = self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        solicitacao_id = response.data['id']
        
        detail_response = self.client.get(f'{self.list_url}{solicitacao_id}/')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['id'], solicitacao_id)
    
    def test_atualizar_solicitacao(self):
        """Testa atualização de solicitação"""
        response = self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        solicitacao_id = response.data['id']
        
        update_payload = {'titulo': 'Férias Atualizadas'}
        update_response = self.client.patch(
            f'{self.list_url}{solicitacao_id}/',
            update_payload,
            format='json'
        )
        
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['titulo'], 'Férias Atualizadas')
    
    def test_excluir_solicitacao(self):
        """Testa exclusão de solicitação"""
        response = self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        solicitacao_id = response.data['id']
        
        delete_response = self.client.delete(f'{self.list_url}{solicitacao_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_aprovar_solicitacao(self):
        """Testa aprovação de solicitação via API"""
        response = self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        solicitacao_id = response.data['id']
        
        aprovar_response = self.client.post(
            f'{self.list_url}{solicitacao_id}/aprovar/',
            {'observacoes': 'Aprovado'},
            format='json'
        )
        
        self.assertEqual(aprovar_response.status_code, status.HTTP_200_OK)
        self.assertEqual(aprovar_response.data['solicitacao']['status'], 'aprovado')
    
    def test_rejeitar_solicitacao(self):
        """Testa rejeição de solicitação via API"""
        response = self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        solicitacao_id = response.data['id']
        
        rejeitar_response = self.client.post(
            f'{self.list_url}{solicitacao_id}/rejeitar/',
            {'observacoes': 'Rejeitado'},
            format='json'
        )
        
        self.assertEqual(rejeitar_response.status_code, status.HTTP_200_OK)
        self.assertEqual(rejeitar_response.data['solicitacao']['status'], 'rejeitado')
    
    def test_cancelar_solicitacao(self):
        """Testa cancelamento de solicitação via API"""
        response = self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        solicitacao_id = response.data['id']
        
        cancelar_response = self.client.post(
            f'{self.list_url}{solicitacao_id}/cancelar/',
            {'observacoes': 'Cancelado'},
            format='json'
        )
        
        self.assertEqual(cancelar_response.status_code, status.HTTP_200_OK)
        self.assertEqual(cancelar_response.data['solicitacao']['status'], 'cancelado')
    
    def test_estatisticas(self):
        """Testa endpoint de estatísticas"""
        # Criar algumas solicitações
        self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        self.client.post(self.list_url, self.valid_reembolso_payload, format='json')
        
        response = self.client.get(f'{self.list_url}estatisticas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertIn('por_tipo', response.data)
        self.assertIn('por_status', response.data)
        self.assertEqual(response.data['total'], 2)
    
    def test_filtrar_por_tipo(self):
        """Testa filtro por tipo de solicitação"""
        self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        self.client.post(self.list_url, self.valid_reembolso_payload, format='json')
        
        response = self.client.get(f'{self.list_url}?tipo=ferias')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['tipo'], 'ferias')
    
    def test_filtrar_por_status(self):
        """Testa filtro por status"""
        response = self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        
        filter_response = self.client.get(f'{self.list_url}?status=pendente')
        self.assertEqual(filter_response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(filter_response.data['results']) > 0)
    
    def test_buscar_por_solicitante(self):
        """Testa busca por nome do solicitante"""
        self.client.post(self.list_url, self.valid_ferias_payload, format='json')
        
        response = self.client.get(f'{self.list_url}?search=Carlos')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
    
    def test_paginacao(self):
        """Testa paginação"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

