from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from config.db import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    cuenta = relationship("Cuenta", backref="cliente")
    categoria_cliente = relationship("CategoriaCliente", backref="cliente")


class Cuenta(Base):
    __tablename__ = "cuenta"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)

    movimiento = relationship("Movimiento", backref="cuenta")


class Movimiento(Base):
    __tablename__ = "movimiento"

    id = Column(Integer, primary_key=True, index=True)
    id_cuenta= Column(Integer, ForeignKey('cuenta.id'), nullable=False)
    tipo = Column(Boolean, default=True)
    importe = Column(Float(precision=2), nullable=False)
    fecha = Column(DateTime, unique=False)


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    categoria_cliente = relationship("CategoriaCliente", backref="categoria")


class CategoriaCliente(Base):
    __tablename__ = "categoria_cliente"

    id = Column(Integer, primary_key=True, index=True)
    id_categoria = Column(Integer, ForeignKey('categoria.id'), nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)

