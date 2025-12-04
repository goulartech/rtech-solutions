"""
Views for the solicitations app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Request
from .serializers import (
    RequestSerializer,
    RequestCreateSerializer,
    RequestUpdateSerializer,
    RequestListSerializer,
    RequestAcaoSerializer,
)
from .filters import RequestFilter


class RequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para gerenciamento de solicitações internas.
    
    Fornece operações CRUD completas e ações customizadas para:
    - Listar todas as solicitações com filtros avançados
    - Criar nova solicitação
    - Visualizar detalhes de uma solicitação
    - Atualizar solicitação existente
    - Excluir solicitação
    - Aprovar solicitação
    - Rejeitar solicitação
    - Cancelar solicitação
    - Obter estatísticas das solicitações
    """
    queryset = Request.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RequestFilter
    search_fields = ['titulo', 'descricao', 'solicitante']
    ordering_fields = ['data_criacao', 'data_atualizacao', 'data_inicio', 'valor']
    ordering = ['-data_criacao']
    
    def get_serializer_class(self):
        """
        Retorna o serializer apropriado baseado na ação
        """
        if self.action == 'create':
            return RequestCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RequestUpdateSerializer
        elif self.action == 'list':
            return RequestListSerializer
        elif self.action in ['aprovar', 'rejeitar', 'cancelar']:
            return RequestAcaoSerializer
        return RequestSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Cria uma nova solicitação
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Retorna o objeto completo usando o RequestSerializer
        headers = self.get_success_headers(serializer.data)
        output_serializer = RequestSerializer(serializer.instance)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """
        Atualiza uma solicitação existente
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Retorna o objeto completo usando o RequestSerializer
        output_serializer = RequestSerializer(serializer.instance)
        return Response(output_serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Exclui uma solicitação
        """
        instance = self.get_object()
        
        # Validação: não permite excluir solicitações aprovadas
        if instance.status == Request.STATUS_APROVADO:
            return Response(
                {'detail': 'Não é possível excluir uma solicitação aprovada.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        """
        Aprova uma solicitação específica.
        
        Corpo da requisição (opcional):
        {
            "observacoes": "Motivo da aprovação"
        }
        """
        solicitacao = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            observacoes = serializer.validated_data.get('observacoes', '')
            solicitacao.aprovar(observacoes)
            output_serializer = RequestSerializer(solicitacao)
            return Response(
                {
                    'detail': 'Solicitação aprovada com sucesso.',
                    'solicitacao': output_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def rejeitar(self, request, pk=None):
        """
        Rejeita uma solicitação específica.
        
        Corpo da requisição (opcional):
        {
            "observacoes": "Motivo da rejeição"
        }
        """
        solicitacao = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            observacoes = serializer.validated_data.get('observacoes', '')
            solicitacao.rejeitar(observacoes)
            output_serializer = RequestSerializer(solicitacao)
            return Response(
                {
                    'detail': 'Solicitação rejeitada.',
                    'solicitacao': output_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Cancela uma solicitação específica.
        
        Corpo da requisição (opcional):
        {
            "observacoes": "Motivo do cancelamento"
        }
        """
        solicitacao = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            observacoes = serializer.validated_data.get('observacoes', '')
            solicitacao.cancelar(observacoes)
            output_serializer = RequestSerializer(solicitacao)
            return Response(
                {
                    'detail': 'Solicitação cancelada.',
                    'solicitacao': output_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        Retorna estatísticas das solicitações.
        
        Resposta:
        {
            "total": 100,
            "por_tipo": {
                "ferias": 40,
                "reembolso": 35,
                "treinamento": 25
            },
            "por_status": {
                "pendente": 20,
                "em_analise": 15,
                "aprovado": 50,
                "rejeitado": 10,
                "cancelado": 5
            },
            "valor_total_aprovado": 150000.00
        }
        """
        from django.db.models import Count, Sum, Q
        
        queryset = self.filter_queryset(self.get_queryset())
        
        # Total de solicitações
        total = queryset.count()
        
        # Contagem por tipo
        por_tipo = dict(
            queryset.values_list('tipo')
            .annotate(count=Count('id'))
            .order_by('tipo')
        )
        
        # Contagem por status
        por_status = dict(
            queryset.values_list('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        
        # Valor total aprovado
        valor_total_aprovado = queryset.filter(
            status=Request.STATUS_APROVADO
        ).aggregate(
            total=Sum('valor')
        )['total'] or 0
        
        return Response({
            'total': total,
            'por_tipo': por_tipo,
            'por_status': por_status,
            'valor_total_aprovado': float(valor_total_aprovado),
        })