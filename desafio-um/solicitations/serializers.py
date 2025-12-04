"""
Serializers para a app solicitations
"""

from rest_framework import serializers
from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    """
    Serializer completo para o modelo Request
    """
    duracao_dias = serializers.ReadOnlyField()
    pode_ser_cancelada = serializers.ReadOnlyField()
    pode_ser_aprovada = serializers.ReadOnlyField()
    
    # Campos de display (human-readable)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Request
        fields = [
            'id',
            'tipo',
            'tipo_display',
            'titulo',
            'descricao',
            'status',
            'status_display',
            'valor',
            'data_inicio',
            'data_fim',
            'solicitante',
            'observacoes',
            'data_criacao',
            'data_atualizacao',
            'duracao_dias',
            'pode_ser_cancelada',
            'pode_ser_aprovada',
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao']
    
    def validate(self, attrs):
        """
        Validações customizadas do serializer
        """
        tipo = attrs.get('tipo')
        valor = attrs.get('valor')
        data_inicio = attrs.get('data_inicio')
        data_fim = attrs.get('data_fim')
        
        # Se está atualizando, pega valores do objeto existente se não foram fornecidos
        if self.instance:
            tipo = tipo or self.instance.tipo
            valor = valor if 'valor' in attrs else self.instance.valor
            data_inicio = data_inicio if 'data_inicio' in attrs else self.instance.data_inicio
            data_fim = data_fim if 'data_fim' in attrs else self.instance.data_fim
        
        # Validar valor para reembolsos e treinamentos
        if tipo in [Request.TIPO_REEMBOLSO, Request.TIPO_TREINAMENTO]:
            if valor is None:
                raise serializers.ValidationError({
                    'valor': f'O campo valor é obrigatório para solicitações de tipo "{Request.TIPO_CHOICES[next(i for i, c in enumerate(Request.TIPO_CHOICES) if c[0] == tipo)][1]}".'
                })
            if valor <= 0:
                raise serializers.ValidationError({
                    'valor': 'O valor deve ser maior que zero.'
                })
        
        # Validar datas para férias e treinamentos
        if tipo in [Request.TIPO_FERIAS, Request.TIPO_TREINAMENTO]:
            if not data_inicio:
                raise serializers.ValidationError({
                    'data_inicio': f'A data de início é obrigatória para solicitações de tipo "{Request.TIPO_CHOICES[next(i for i, c in enumerate(Request.TIPO_CHOICES) if c[0] == tipo)][1]}".'
                })
            if not data_fim:
                raise serializers.ValidationError({
                    'data_fim': f'A data de término é obrigatória para solicitações de tipo "{Request.TIPO_CHOICES[next(i for i, c in enumerate(Request.TIPO_CHOICES) if c[0] == tipo)][1]}".'
                })
            if data_inicio and data_fim and data_inicio > data_fim:
                raise serializers.ValidationError({
                    'data_fim': 'A data de término deve ser posterior à data de início.'
                })
        
        return attrs


class RequestCreateSerializer(RequestSerializer):
    """
    Serializer específico para criação de solicitações
    """
    class Meta(RequestSerializer.Meta):
        fields = [
            'tipo',
            'titulo',
            'descricao',
            'valor',
            'data_inicio',
            'data_fim',
            'solicitante',
            'observacoes',
        ]


class RequestUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para atualização de solicitações
    Permite atualização parcial de campos
    """
    class Meta:
        model = Request
        fields = [
            'titulo',
            'descricao',
            'valor',
            'data_inicio',
            'data_fim',
            'observacoes',
        ]
    
    def validate(self, attrs):
        """
        Validações para atualização
        """
        # Não permite atualização de solicitações já finalizadas
        if self.instance.status in [Request.STATUS_APROVADO, Request.STATUS_REJEITADO, Request.STATUS_CANCELADO]:
            raise serializers.ValidationError(
                f'Não é possível atualizar uma solicitação com status "{self.instance.get_status_display()}".'
            )
        
        return super().validate(attrs)


class RequestListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para listagem de solicitações
    Retorna apenas campos essenciais
    """
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    duracao_dias = serializers.ReadOnlyField()
    
    class Meta:
        model = Request
        fields = [
            'id',
            'tipo',
            'tipo_display',
            'titulo',
            'status',
            'status_display',
            'valor',
            'solicitante',
            'data_criacao',
            'duracao_dias',
        ]


class RequestAcaoSerializer(serializers.Serializer):
    """
    Serializer para ações de aprovação, rejeição e cancelamento
    """
    observacoes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        help_text='Observações sobre a ação realizada'
    )
