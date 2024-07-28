import random
import re
import string
import sys
from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.elemento import Elemento, TipoElemento
from src.modelo.declarative_base import engine, Base, session
from sqlalchemy import exists
from sqlalchemy.orm import joinedload
from urllib.parse import urlparse
from dateutil.parser import parse
import datetime

class Logica(FachadaCajaDeSeguridad):
    def __init__(self):
        Base.metadata.create_all(engine)

        self.clave_maestra = 'clave'
        
    def validar_crear_editar_clave(self, nombre, clave, pista):
        if nombre is None or len(nombre) == 0:
            return "El campo nombre no puede estar vacío"
        
        if clave is None  or len(clave) == 0:
            return "El campo clave no puede estar vacío"
        
        if pista is None or len(pista) == 0:
            return "El campo pista no puede estar vacío"
        
        return ""

    def dar_claves_favoritas(self):
        self.claves_favoritas = session.query(ClaveFavorita).all()
        return self.claves_favoritas
    
    def crear_clave(self, nombre, clave, pista):
        error = self.validar_crear_editar_clave(nombre, clave, pista)
        if len(error) > 0:
            return error
        
        clave_existente = session.query(ClaveFavorita).filter(ClaveFavorita.nombre == nombre).first()
        if clave_existente is not None:
            return "Ya existe una clave con ese nombre "
        
        nueva_clave = ClaveFavorita(nombre=nombre, clave=clave, pista=pista)
        session.add(nueva_clave)
        session.commit()
        return nueva_clave