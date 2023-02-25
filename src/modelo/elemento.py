import enum

from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship

from .declarative_base import Base


class TipoElemento(enum.Enum):
    LOGIN = 1
    SECRETO = 2
    IDENTIFICACION = 3
    TARJETA = 4


class Elemento(Base):
    __tablename__ = 'elemento'

    id = Column(Integer, primary_key=True)
    nombreElemento = Column(String)
    tipo = Column(Enum(TipoElemento))
    email = Column(String)
    usuario = Column(String)
    url = Column(String)
    notas = Column(String)
    numero = Column(String)
    nombre = Column(String)
    cvv = Column(Integer)
    direccion = Column(String)
    telefono = Column(String)
    secreto = Column(String)
    fechaNacimiento = Column(Date)
    fechaExp = Column(Date)
    fechaVenc = Column(Date)
    claveFavorita = relationship('claveFavorita', uselist=False)