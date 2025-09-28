from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4


class SchemaVagas(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200, description="Título da vaga")
    descricao: str = Field(..., min_length=1, description="Descrição detalhada da vaga")
    requisitos: List[str] = Field(..., description="Lista de requisitos para a vaga")
    salario: Optional[str] = Field(None, description="Faixa salarial da vaga")
    localizacao: Optional[str] = Field(None, description="Localização da vaga")
    tipo_contrato: str = Field(..., description="Tipo de contrato (CLT, PJ, etc.)")
    nivel_experiencia: str = Field(..., description="Nível de experiência (Júnior, Pleno, Sênior)")
    modalidade: str = Field(..., description="Modalidade (Presencial, Híbrido, Remoto)")
    ativa: bool = Field(default=True, description="Status da vaga (ativa/inativa)")


class VagaCreate(SchemaVagas):
    pass


class VagaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descricao: Optional[str] = Field(None, min_length=1)
    requisitos: Optional[List[str]] = Field(None)
    salario: Optional[str] = Field(None)
    localizacao: Optional[str] = Field(None)
    tipo_contrato: Optional[str] = Field(None)
    nivel_experiencia: Optional[str] = Field(None)
    modalidade: Optional[str] = Field(None)
    ativa: Optional[bool] = Field(None)


class VagaInDB(SchemaVagas):
    id: UUID = Field(default_factory=uuid4)
    criada_em: datetime = Field(default_factory=datetime.utcnow)
    atualizada_em: datetime = Field(default_factory=datetime.utcnow)


class VagaResponse(VagaInDB):
    class Config:
        from_attributes = True


class VagasListResponse(BaseModel):
    vagas: List[VagaResponse]
    total: int
    pagina: int
    por_pagina: int