"""
Filtros customizados para a app solicitations
"""

import django_filters
from .models import Request


class RequestFilter(django_filters.FilterSet):
    """
    Filtros avançados para solicitações
    """
    # Filtros por tipo e status (múltiplos valores)
    tipo = django_filters.MultipleChoiceFilter(
        choices=Request.TIPO_CHOICES,
        help_text='Filtrar por tipo de solicitação (pode usar múltiplos valores)'
    )
    
    status = django_filters.MultipleChoiceFilter(
        choices=Request.STATUS_CHOICES,
        help_text='Filtrar por status (pode usar múltiplos valores)'
    )
    
    # Filtros de data
    data_criacao_min = django_filters.DateFilter(
        field_name='data_criacao',
        lookup_expr='gte',
        help_text='Data de criação mínima (formato: YYYY-MM-DD)'
    )
    
    data_criacao_max = django_filters.DateFilter(
        field_name='data_criacao',
        lookup_expr='lte',
        help_text='Data de criação máxima (formato: YYYY-MM-DD)'
    )
    
    data_inicio_min = django_filters.DateFilter(
        field_name='data_inicio',
        lookup_expr='gte',
        help_text='Data de início mínima (formato: YYYY-MM-DD)'
    )
    
    data_inicio_max = django_filters.DateFilter(
        field_name='data_inicio',
        lookup_expr='lte',
        help_text='Data de início máxima (formato: YYYY-MM-DD)'
    )
    
    # Filtros de valor
    valor_min = django_filters.NumberFilter(
        field_name='valor',
        lookup_expr='gte',
        help_text='Valor mínimo'
    )
    
    valor_max = django_filters.NumberFilter(
        field_name='valor',
        lookup_expr='lte',
        help_text='Valor máximo'
    )
    
    # Filtro por solicitante
    solicitante = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text='Buscar por nome do solicitante (case-insensitive)'
    )
    
    class Meta:
        model = Request
        fields = ['tipo', 'status', 'solicitante']
