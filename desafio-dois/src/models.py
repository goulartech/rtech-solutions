"""
Modelos de dados da aplicação com validação usando Pydantic
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, field_serializer


class StatusSolicitacao(str, Enum):
    """Enum para status das solicitações"""
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class TipoSolicitacao(str, Enum):
    """Enum para tipos de solicitações"""
    MANUTENCAO = "manutencao"
    SUPORTE = "suporte"
    DESENVOLVIMENTO = "desenvolvimento"
    CONSULTA = "consulta"
    OUTROS = "outros"


class SolicitacaoBase(BaseModel):
    """Schema base para solicitação"""
    tipo: TipoSolicitacao = Field(..., description="Tipo da solicitação")
    descricao: str = Field(..., min_length=10, max_length=500, description="Descrição da solicitação")
    status: StatusSolicitacao = Field(default=StatusSolicitacao.PENDENTE, description="Status da solicitação")

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: str) -> str:
        """Valida e normaliza a descrição"""
        v = v.strip()
        if not v:
            raise ValueError("Descrição não pode estar vazia")
        return v


class SolicitacaoCreate(SolicitacaoBase):
    """Schema para criação de solicitação"""
    pass


class SolicitacaoUpdate(BaseModel):
    """Schema para atualização de solicitação"""
    tipo: Optional[TipoSolicitacao] = None
    descricao: Optional[str] = Field(None, min_length=10, max_length=500)
    status: Optional[StatusSolicitacao] = None

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: Optional[str]) -> Optional[str]:
        """Valida e normaliza a descrição"""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Descrição não pode estar vazia")
        return v


class Solicitacao(SolicitacaoBase):
    """Schema completo da solicitação"""
    id: int = Field(..., description="ID único da solicitação")
    data_criacao: datetime = Field(default_factory=datetime.now, description="Data de criação")
    data_atualizacao: datetime = Field(default_factory=datetime.now, description="Data da última atualização")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "tipo": "suporte",
                "descricao": "Solicitação de suporte técnico para problema no sistema",
                "status": "pendente",
                "data_criacao": "2025-12-04T10:00:00",
                "data_atualizacao": "2025-12-04T10:00:00"
            }
        }
    )

    @field_serializer('data_criacao', 'data_atualizacao')
    def serialize_datetime(self, dt: datetime) -> str:
        """Serializa datetime para ISO format"""
        return dt.isoformat()
