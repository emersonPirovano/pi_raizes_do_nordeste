
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ClienteBase(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    email: str | None = Field(default=None, max_length=150)
    telefone: str | None = Field(default=None, max_length=20)
    data_nascimento: date | None = None
    consentimento_lgpd: bool = False


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    email: str | None = Field(default=None, max_length=150)
    telefone: str | None = Field(default=None, max_length=20)
    data_nascimento: date | None = None
    consentimento_lgpd: bool | None = None


class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
