import enum

from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.modelo.clave_favorita import ClaveFavorita

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
    clave_favorita_id = Column(Integer, ForeignKey('clave_favorita.id'), nullable=True)
    claveFavorita = relationship("ClaveFavorita", foreign_keys=[clave_favorita_id])

    def __getitem__(self, indice):
        if indice == 'nombreElemento':
            return self.nombreElemento
        if indice == 'tipo':
            if self.tipo == TipoElemento.LOGIN:
                return "Login"
            if self.tipo == TipoElemento.IDENTIFICACION:
                return "Ids"
            if self.tipo == TipoElemento.TARJETA:
                return "Tarjeta"
            if self.tipo == TipoElemento.SECRETO:
                return "Secreto"
            return self.tipo
        if indice == 'email':
            return self.email
        if indice == 'usuario':
            return self.usuario
        if indice == 'url':
            return self.url
        if indice == 'notas':
            return self.notas
        if indice == 'numero':
            return self.numero
        if indice == 'nombre':
            return self.nombre
        if indice == 'cvv':
            return self.cvv
        if indice == 'direccion':
            return self.direccion
        if indice == 'telefono':
            return self.telefono
        if indice == 'secreto':
            return self.secreto
        if indice == 'fechaNacimiento':
            return self.fechaNacimiento
        if indice == 'fechaExp':
            return self.fechaExp
        if indice == 'fechaVen':
            return self.fechaVenc
        if indice == 'claveFavorita':
            return self.claveFavorita