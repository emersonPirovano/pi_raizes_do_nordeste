from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LojaBase(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    cnpj: str = Field(min_length=14, max_length=14)

    telefone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=150)

    cep: str | None = Field(default=None, max_length=8)
    logradouro: str | None = Field(default=None, max_length=150)
    numero: str | None = Field(default=None, max_length=20)
    complemento: str | None = Field(default=None, max_length=100)
    bairro: str | None = Field(default=None, max_length=100)
    cidade: str | None = Field(default=None, max_length=100)
    uf: str | None = Field(default=None, max_length=2)


class LojaCreate(LojaBase):
    pass


class LojaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=150)
    telefone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=150)

    cep: str | None = Field(default=None, max_length=8)
    logradouro: str | None = Field(default=None, max_length=150)
    numero: str | None = Field(default=None, max_length=20)
    complemento: str | None = Field(default=None, max_length=100)
    bairro: str | None = Field(default=None, max_length=100)
    cidade: str | None = Field(default=None, max_length=100)
    uf: str | None = Field(default=None, max_length=2)

    ativa: bool | None = None


class LojaResponse(LojaBase):
    id: int
    ativa: bool
    criada_em: datetime

    model_config = ConfigDict(from_attributes=True)
    