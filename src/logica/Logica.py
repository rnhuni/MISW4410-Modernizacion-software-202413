import random
import re
import string
import sys
from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.elemento import Elemento, TipoElemento
from src.modelo.declarative_base import engine, Base, session
from sqlalchemy import exists
from urllib.parse import urlparse

class Logica(FachadaCajaDeSeguridad):        

    def __init__(self):
        if 'unittest' in sys.modules.keys():
            Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        self.clave_maestra = 'clave'

        self.claves_favoritas = []

        self.elementos = []

    def dar_claveMaestra(self):
        return self.clave_maestra
    
    def dar_claves_favoritas(self):
        self.claves_favoritas = session.query(ClaveFavorita).all()
        return self.claves_favoritas
    
    def dar_elementos(self):
        self.elementos = session.query(Elemento).all()
        return self.elementos
    
    def crear_clave(self, nombre, clave, pista):
        if nombre is None or clave is None or pista is None or clave != pista:
            return False
        
        clave_existente = session.query(ClaveFavorita).filter(ClaveFavorita.nombre == nombre).first()
        if clave_existente is not None:
            return False
        
        nueva_clave = ClaveFavorita(nombre=nombre, clave=clave, pista=pista)
        session.add(nueva_clave)
        session.commit()
        session.close()
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
    
    def es_email(self, email):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return bool(re.match(pattern, email))
    
    def es_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.scheme and parsed_url.netloc
    
    def crear_login(self, nombre, email, usuario, password, url, notas):
        if nombre is None or email is None or usuario is None or password is None or url is None or notas is None:
            return False
        
        if len(nombre) > 255 or len(email) > 255 or len(usuario) > 255 or len(url) > 255:
            return False
        
        if len(notas) > 512:
            return False
        
        if not self.es_email(email): 
            return False
        
        if not self.es_url(url): 
            return False
        
        existe_clave = session.query(exists().where(ClaveFavorita.id == password)).scalar()
        if not existe_clave: 
            return False
        
        existe_nombre = session.query(exists().where(Elemento.nombreElemento == nombre)).scalar()
        if existe_nombre: 
            return False
        
        nuevo_login = Elemento(tipo=TipoElemento.LOGIN, nombreElemento=nombre, email=email, usuario=usuario, clave_favorita_id=password, url=url, notas=notas)
        session.add(nuevo_login)
        session.commit()
        session.close()

        return True
    
    def dar_clave(self, nombre_clave):
        self.claves_favoritas = session.query(ClaveFavorita).all()

        i = 0
        while i < len(self.claves_favoritas):
            if self.claves_favoritas[i]['nombre'] == nombre_clave:
                return self.claves_favoritas[i]['id']
            i = i+1

        return None

    def editar_clave(self, id,  nombre, clave, pista):
        if id is None or nombre is None or clave is None or pista is None:
            return False
                
        return True
    
    def contar_claves_inseguras(self, clavesFavoritas):
        cantidad = 0
        for clave in clavesFavoritas:
            if self.es_clave_segura(clave.clave):
                cantidad += 1
                
        return cantidad