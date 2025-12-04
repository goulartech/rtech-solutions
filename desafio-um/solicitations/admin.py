"""
Admin registration for the requests app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """
    Configuração customizada do Admin para o modelo Request
    """
    # Campos exibidos na lista
    list_display = [
        'id',
        'tipo_display',
        'titulo',
        'solicitante',
        'status_badge',
        'valor_formatado',
        'duracao_dias',
        'data_criacao',
    ]
    
    # Filtros laterais
    list_filter = [
        'tipo',
        'status',
        'data_criacao',
        'data_inicio',
    ]
    
    # Campos de busca
    search_fields = [
        'titulo',
        'descricao',
        'solicitante',
        'observacoes',
    ]
    
    # Campos somente leitura
    readonly_fields = [
        'id',
        'data_criacao',
        'data_atualizacao',
        'duracao_dias',
        'pode_ser_cancelada',
        'pode_ser_aprovada',
    ]
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tipo', 'titulo', 'descricao', 'solicitante')
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes')
        }),
        ('Valores e Datas', {
            'fields': ('valor', 'data_inicio', 'data_fim')
        }),
        ('Informações do Sistema', {
            'fields': (
                'id',
                'data_criacao',
                'data_atualizacao',
                'duracao_dias',
                'pode_ser_cancelada',
                'pode_ser_aprovada',
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Ordenação padrão
    ordering = ['-data_criacao']
    
    # Paginação
    list_per_page = 25
    
    # Ações customizadas
    actions = ['aprovar_solicitacoes', 'rejeitar_solicitacoes', 'cancelar_solicitacoes']
    
    def tipo_display(self, obj):
        """Exibe o tipo formatado"""
        return obj.get_tipo_display()
    tipo_display.short_description = 'Tipo'
    tipo_display.admin_order_field = 'tipo'
    
    def status_badge(self, obj):
        """Exibe o status com badge colorido"""
        colors = {
            Request.STATUS_PENDENTE: '#ffc107',
            Request.STATUS_EM_ANALISE: '#17a2b8',
            Request.STATUS_APROVADO: '#28a745',
            Request.STATUS_REJEITADO: '#dc3545',
            Request.STATUS_CANCELADO: '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def valor_formatado(self, obj):
        """Exibe o valor formatado em reais"""
        if obj.valor:
            return f'R$ {obj.valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        return '-'
    valor_formatado.short_description = 'Valor'
    valor_formatado.admin_order_field = 'valor'
    
    # Ações em massa
    def aprovar_solicitacoes(self, request, queryset):
        """Aprova solicitações selecionadas"""
        count = 0
        for solicitacao in queryset:
            if solicitacao.pode_ser_aprovada:
                try:
                    solicitacao.aprovar('Aprovado em massa pelo admin')
                    count += 1
                except ValueError:
                    pass
        self.message_user(request, f'{count} solicitação(ões) aprovada(s) com sucesso.')
    aprovar_solicitacoes.short_description = 'Aprovar solicitações selecionadas'
    
    def rejeitar_solicitacoes(self, request, queryset):
        """Rejeita solicitações selecionadas"""
        count = 0
        for solicitacao in queryset:
            if solicitacao.pode_ser_aprovada:
                try:
                    solicitacao.rejeitar('Rejeitado em massa pelo admin')
                    count += 1
                except ValueError:
                    pass
        self.message_user(request, f'{count} solicitação(ões) rejeitada(s).')
    rejeitar_solicitacoes.short_description = 'Rejeitar solicitações selecionadas'
    
    def cancelar_solicitacoes(self, request, queryset):
        """Cancela solicitações selecionadas"""
        count = 0
        for solicitacao in queryset:
            if solicitacao.pode_ser_cancelada:
                try:
                    solicitacao.cancelar('Cancelado em massa pelo admin')
                    count += 1
                except ValueError:
                    pass
        self.message_user(request, f'{count} solicitação(ões) cancelada(s).')
    cancelar_solicitacoes.short_description = 'Cancelar solicitações selecionadas'

