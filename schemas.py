from pydantic import BaseModel, Field

class Persona(BaseModel):

    nome: str
    classe: str
    level: int = Field(ge=0, le=100)

class Boss(BaseModel):

    nome: str
    vivo_derrotado: bool

class Armamento(BaseModel):

    tipo_arma: str

class Combate(BaseModel):

    personagem_id: int
    boss_id: int