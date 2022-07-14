from pydantic import BaseModel
from datetime import datetime
from typing import List


class ClienteBase(BaseModel):

    nombre: str


class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase):
    id: int

    class Config:
        orm_mode = True


class MovimientoBase(BaseModel):
    id_cuenta: int
    tipo: bool
    importe: float
    fecha: datetime


class MovimientoCreate(MovimientoBase):
    pass


class Movimiento(MovimientoBase):
    id: int


    class Config:
        orm_mode = True


class CategoriaClienteBase(BaseModel):

    id_categoria: int
    id_cliente: int


class CategoriaClienteCreate(CategoriaClienteBase):
    pass


class CategoriaCliente(CategoriaClienteBase):
    id: int

    class Config:
        orm_mode = True