from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad
from src.modelo.declarative_base import engine, Base, session

class Logica(FachadaCajaDeSeguridad):        

    def __init__(self):
        Base.metadata.create_all(engine)

        self.clave_maestra = 'clave'

        self.claves_favoritas = []

    def dar_claveMaestra(self):
        return self.clave_maestra
    
    def dar_claves_favoritas(self):
        return self.claves_favoritas
    
    def crear_clave(self, nombre, clave, pista):
        return None
    
    def generar_clave(self):
        return None
    
    def dar_elementos(self):
        return None
    