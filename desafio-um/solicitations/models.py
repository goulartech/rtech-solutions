"""
Models for the solicitations app
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Request(models.Model):
    """
    Modelo para representar solicitações internas da empresa.
    Suporta diferentes tipos de solicitações como férias, reembolsos e treinamentos.
    """
    
    # Choices para tipo de solicitação
    TIPO_FERIAS = 'ferias'
    TIPO_REEMBOLSO = 'reembolso'
    TIPO_TREINAMENTO = 'treinamento'
    
    TIPO_CHOICES = [
        (TIPO_FERIAS, 'Férias'),
        (TIPO_REEMBOLSO, 'Reembolso'),
        (TIPO_TREINAMENTO, 'Treinamento'),
    ]
    
    # Choices para status da solicitação
    STATUS_PENDENTE = 'pendente'
    STATUS_EM_ANALISE = 'em_analise'
    STATUS_APROVADO = 'aprovado'
    STATUS_REJEITADO = 'rejeitado'
    STATUS_CANCELADO = 'cancelado'
    
    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_EM_ANALISE, 'Em Análise'),
        (STATUS_APROVADO, 'Aprovado'),
        (STATUS_REJEITADO, 'Rejeitado'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]
    
    # Campos da solicitação
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Solicitação',
        help_text='Tipo da solicitação: férias, reembolso ou treinamento'
    )
    
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título descritivo da solicitação'
    )
    
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição detalhada da solicitação'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
        verbose_name='Status',
        help_text='Status atual da solicitação'
    )
    
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)],
        verbose_name='Valor',
        help_text='Valor monetário (obrigatório para reembolsos e treinamentos)'
    )
    
    data_inicio = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Início',
        help_text='Data de início (obrigatório para férias e treinamentos)'
    )
    
    data_fim = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Término',
        help_text='Data de término (obrigatório para férias e treinamentos)'
    )
    
    solicitante = models.CharField(
        max_length=200,
        verbose_name='Solicitante',
        help_text='Nome do colaborador solicitante'
    )
    
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações',
        help_text='Observações adicionais ou motivo de rejeição'
    )
    
    # Campos de auditoria
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Data de Atualização'
    )
    
    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['tipo', 'status']),
            models.Index(fields=['solicitante']),
            models.Index(fields=['-data_criacao']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo} ({self.get_status_display()})"
    
    def clean(self):
        """
        Validações customizadas do modelo
        """
        from django.core.exceptions import ValidationError
        
        # Validar valor para reembolsos e treinamentos
        if self.tipo in [self.TIPO_REEMBOLSO, self.TIPO_TREINAMENTO] and not self.valor:
            raise ValidationError({
                'valor': f'O campo valor é obrigatório para solicitações de {self.get_tipo_display().lower()}.'
            })
        
        # Validar datas para férias e treinamentos
        if self.tipo in [self.TIPO_FERIAS, self.TIPO_TREINAMENTO]:
            if not self.data_inicio:
                raise ValidationError({
                    'data_inicio': f'A data de início é obrigatória para solicitações de {self.get_tipo_display().lower()}.'
                })
            if not self.data_fim:
                raise ValidationError({
                    'data_fim': f'A data de término é obrigatória para solicitações de {self.get_tipo_display().lower()}.'
                })
            if self.data_inicio and self.data_fim and self.data_inicio > self.data_fim:
                raise ValidationError({
                    'data_fim': 'A data de término deve ser posterior à data de início.'
                })
    
    def save(self, *args, **kwargs):
        """
        Override do método save para executar validações
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def duracao_dias(self):
        """
        Calcula a duração em dias para solicitações com data de início e fim
        """
        if self.data_inicio and self.data_fim:
            return (self.data_fim - self.data_inicio).days + 1
        return None
    
    @property
    def pode_ser_cancelada(self):
        """
        Verifica se a solicitação pode ser cancelada
        """
        return self.status in [self.STATUS_PENDENTE, self.STATUS_EM_ANALISE]
    
    @property
    def pode_ser_aprovada(self):
        """
        Verifica se a solicitação pode ser aprovada
        """
        return self.status in [self.STATUS_PENDENTE, self.STATUS_EM_ANALISE]
    
    def aprovar(self, observacoes=''):
        """
        Aprova a solicitação
        """
        if not self.pode_ser_aprovada:
            raise ValueError(f'Solicitação com status {self.get_status_display()} não pode ser aprovada.')
        self.status = self.STATUS_APROVADO
        if observacoes:
            self.observacoes = observacoes
        self.save()
    
    def rejeitar(self, observacoes=''):
        """
        Rejeita a solicitação
        """
        if not self.pode_ser_aprovada:
            raise ValueError(f'Solicitação com status {self.get_status_display()} não pode ser rejeitada.')
        self.status = self.STATUS_REJEITADO
        if observacoes:
            self.observacoes = observacoes
        self.save()
    
    def cancelar(self, observacoes=''):
        """
        Cancela a solicitação
        """
        if not self.pode_ser_cancelada:
            raise ValueError(f'Solicitação com status {self.get_status_display()} não pode ser cancelada.')
        self.status = self.STATUS_CANCELADO
        if observacoes:
            self.observacoes = observacoes
        self.save()
