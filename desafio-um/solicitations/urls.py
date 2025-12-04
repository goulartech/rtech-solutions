"""
URL configuration for solicitations app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequestViewSet


# Configurar roteador do DRF
router = DefaultRouter()
router.register(r'solicitacoes', RequestViewSet, basename='solicitacao')

urlpatterns = [
    path('', include(router.urls)),
]

# Rotas disponíveis:
# GET    /api/v1/solicitacoes/              - Listar todas as solicitações
# POST   /api/v1/solicitacoes/              - Criar nova solicitação
# GET    /api/v1/solicitacoes/{id}/         - Visualizar detalhes de uma solicitação
# PUT    /api/v1/solicitacoes/{id}/         - Atualizar solicitação completa
# PATCH  /api/v1/solicitacoes/{id}/         - Atualizar solicitação parcial
# DELETE /api/v1/solicitacoes/{id}/         - Excluir solicitação
# POST   /api/v1/solicitacoes/{id}/aprovar/ - Aprovar solicitação
# POST   /api/v1/solicitacoes/{id}/rejeitar/ - Rejeitar solicitação
# POST   /api/v1/solicitacoes/{id}/cancelar/ - Cancelar solicitação
# GET    /api/v1/solicitacoes/estatisticas/ - Obter estatísticas

