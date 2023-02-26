import random
import string
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
        if nombre is None or clave is None or pista is None or clave != pista:
            return False
        return True

    def es_clave_segura(selft, clave):
        tiene_mayusculas = False
        tiene_minusculas = False
        tiene_cespeciales = False
        sin_espacios = True

        for c in clave:
            if not tiene_mayusculas and c.isupper():
                tiene_mayusculas = True
            elif not tiene_minusculas and c.islower():
                tiene_minusculas = True
            elif not tiene_cespeciales and c in string.punctuation:
                tiene_cespeciales = True
            elif c.isspace():
                sin_espacios = False
        
        return tiene_mayusculas and tiene_minusculas and tiene_cespeciales and sin_espacios
    
    def generar_clave(self):
        longitud = random.randint(8, 16)
        caracteres_posibles = string.digits + string.punctuation + string.ascii_letters
        
        while True:
            clave_candidata = ''        
            for i in range(longitud):
                clave_candidata += random.choice(caracteres_posibles)
            
            if self.es_clave_segura(clave_candidata):
                return clave_candidata