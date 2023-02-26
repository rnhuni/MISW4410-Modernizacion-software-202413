from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.elemento import Elemento
from src.modelo.declarative_base import engine, Base, session

class Logica(FachadaCajaDeSeguridad):        

    def __init__(self):
        Base.metadata.create_all(engine)

        self.clave_maestra = 'clave'

        self.claves_favoritas = []

        self.elementos = []

    def dar_claveMaestra(self):
        return self.clave_maestra
    
    def dar_claves_favoritas(self):
        self.claves_favoritas = session.query(ClaveFavorita).all()
        return self.claves_favoritas
    
    def crear_clave(self, nombre, clave, pista):
        return None
    
    def generar_clave(self):
        return None
    
    def dar_elementos(self):
        self.elementos = session.query(Elemento).all()
        return self.elementos
    
    def crear_clave(self, nombre, clave, pista):
        if nombre is None or clave is None or pista is None:
            return False
        return True