import enum

from sqlalchemy import Column, Integer, String, String, String
from sqlalchemy.orm import relationship

from .declarative_base import Base


class ClaveFavorita(Base):
    __tablename__ = 'clave_favorita'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    clave = Column(String)
    pista = Column(String)

    def __getitem__(self, indice): # pragma: no cover
        if indice == 'id_clave':
            return self.id
        if indice == 'id':
            return self.id
        if indice == 'nombre':
            return self.nombre
        if indice == 'clave':
            return self.clave
        if indice == 'pista':
            return self.pista