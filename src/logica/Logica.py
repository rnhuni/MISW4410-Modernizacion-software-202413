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
        if 'unittest' in sys.modules.keys():  # pragma: no cover
            Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        self.clave_maestra = 'clave'

        self.claves_favoritas = self.dar_claves_favoritas()

        self.elementos = self.dar_elementos()

    def dar_claveMaestra(self):
        return self.clave_maestra
    
    def dar_claves_favoritas(self):
        self.claves_favoritas = session.query(ClaveFavorita).all()
        return self.claves_favoritas
    
    def dar_elementos(self):
        self.elementos = session.query(Elemento).all()
        return self.elementos
    
    def crear_clave(self, nombre, clave, pista):
        error = self.validar_crear_editar_clave(nombre, clave, pista)
        if len(error) > 0:
            return error
        
        clave_existente = session.query(ClaveFavorita).filter(ClaveFavorita.nombre == nombre).first()
        if clave_existente is not None:
            return "Ya existe una clave con ese nombre"
        
        nueva_clave = ClaveFavorita(nombre=nombre, clave=clave, pista=pista)
        session.add(nueva_clave)
        session.commit()
        return ""

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
        err = self.validar_crear_editar_login(0, nombre, email, usuario, password, url, notas)
        if len(err) > 0:
            return err
        
        nuevo_login = Elemento(tipo=TipoElemento.LOGIN, nombreElemento=nombre, email=email, usuario=usuario, clave_favorita_id=password, url=url, notas=notas)
        session.add(nuevo_login)
        session.commit()

        return ""
    
    def validar_crear_editar_login(self, id, nombre, email, usuario, password, url, notas):
        if nombre is None or len(nombre) == 0:
            return "El campo nombre no puede estar vacío"
        
        if email is None or len(email) == 0:
            return "El campo email no puede estar vacío"
        
        if usuario is None or len(usuario) == 0:
            return "El campo usuario no puede estar vacío"
        
        if url is None or len(url) == 0:
            return "El campo url no puede estar vacío"
        
        if notas is None or len(notas) == 0:
            return "El campo notas no puede estar vacío"
            
        if password is None or len(password) == 0:
            return "El campo password no puede estar vacío"
        
        if len(nombre) > 255 or len(email) > 255 or len(usuario) > 255 or len(url) > 255:
            return "Los campos no puede tener más de 255 caracteres"
        
        if len(notas) > 512:
            return "El campo notas no puede tenes más de 512 caracteres"
        
        if not self.es_email(email): 
            return "El campo email es inválido"
        
        if not self.es_url(url): 
            return "El campo url es inválido"
        
        existe_nombre = session.query(exists().where(Elemento.nombreElemento == nombre)).scalar()
        if existe_nombre: 
            return "Ya existe un elemento con ese nombre"
        
        return ""
    
    def dar_clave(self, nombre_clave):
        self.claves_favoritas = session.query(ClaveFavorita).all()

        i = 0
        while i < len(self.claves_favoritas):
            if self.claves_favoritas[i]['nombre'] == nombre_clave:
                return self.claves_favoritas[i]['id']
            i = i+1

        return None

    def editar_clave(self, id,  nombre, clave, pista):
        if nombre is None or len(nombre) == 0:
            return "El campo nombre no puede estar vacío"
        
        if clave is None  or len(clave) == 0:
            return "El campo clave no puede estar vacío"
        
        if pista is None or len(pista) == 0:
            return "El campo pista no puede estar vacío"
        
        clave_existente = self.claves_favoritas[id]
        existe_nombre = session.query(ClaveFavorita).filter(ClaveFavorita.nombre == nombre).first()
        if existe_nombre:
            if existe_nombre.id != clave_existente.id:
                return "Ya existe una clave con ese nombre"
            
        clave_existente.nombre = nombre
        clave_existente.clave = clave
        clave_existente.pista = pista
       
        session.commit()

        return ""
    
    def contar_claves_inseguras(self, clavesFavoritas):
        cantidad = 0
        for clave in clavesFavoritas:
            if not self.es_clave_segura(clave.clave):
                cantidad += 1

        return cantidad
    
    def calcular_masdeuna(self, elementos):
        cantidad = 0
        usadas = {}
        for elemento in elementos:
            id = elemento.clave_favorita_id
            if id in usadas:
                usadas[id] += 1
                if usadas[id] == 2:
                    cantidad += 1
            else:
                usadas[id] = 1

        return cantidad

    def calcular_r(self, elementos):
        usadas = {}
        r = 1.0
        for elemento in elementos:
            id = elemento.clave_favorita_id
            if id in usadas:
                usadas[id] += 1
                if usadas[id] > 3:
                    return 0.0
                r = 0.5
            else:
                usadas[id] = 1
        return r
    
    def calcular_nivel_seguridad(self, cantidad_claves, inseguras, cantidad_elementos, avencer, R):
        SC = (cantidad_claves - inseguras) * cantidad_claves / 100
        V = (cantidad_elementos - avencer) * cantidad_elementos / 100
        R = R

        return SC + 0.5 + V * 0.2 + R * 0.3
    
    def calcular_avencer(self, elementos): #TODO: pendiente de implementar cuando agregemos las inserciones para todos los tipos de elementos
        return 0
    
    def dar_reporte_seguridad(self):
        claves = self.dar_claves_favoritas()
        elementos = self.dar_elementos()
        cantidad_claves = len(claves)
        inseguras = self.contar_claves_inseguras(claves)

        cantidad_elementos = len(elementos)
        avencer = self.calcular_avencer(elementos)

        masdeuna = self.calcular_masdeuna(elementos)

        R = self.calcular_r(elementos)

        nivel = self.calcular_nivel_seguridad(cantidad_claves, inseguras, cantidad_elementos, avencer, R)

        #Contar por tipos
        login = 0
        ids = 0
        tarjetas = 0
        secretos = 0
        for elemento in self.elementos:
            if elemento.tipo == TipoElemento.LOGIN:
                login += 1
            if elemento.tipo == TipoElemento.IDENTIFICACION:
                ids += 1
            if elemento.tipo == TipoElemento.TARJETA:
                tarjetas += 1
            if elemento.tipo == TipoElemento.SECRETO:
                secretos += 1
        datos_reporte ={}
            
        datos_reporte['logins'] = login
        datos_reporte['ids'] = ids
        datos_reporte['tarjetas'] = tarjetas
        datos_reporte['secretos'] = secretos
        datos_reporte['inseguras'] =inseguras
        datos_reporte['avencer'] = avencer
        datos_reporte['masdeuna'] = masdeuna
        datos_reporte['nivel'] = nivel

        return datos_reporte
    
    def validar_crear_editar_clave(self, nombre, clave, pista):
        if nombre is None or len(nombre) == 0:
            return "El campo nombre no puede estar vacío"
        
        if clave is None  or len(clave) == 0:
            return "El campo clave no puede estar vacío"
        
        if pista is None or len(pista) == 0:
            return "El campo pista no puede estar vacío"
        
        return ""
    
    def eliminar_elemento(self, id):
        elemento = self.elementos[id]
        session.delete(elemento)
        session.commit()
        
        del self.elementos[id]

    def crear_id(self, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        error = self.validar_crear_editar_id(-1, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas)
        if len(error) > 0:
            return error
        
        return ""
    
    def validar_crear_editar_id(self, id, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        if nombre_elemento is None or len(nombre_elemento) == 0:
            return "El campo nombre elemento no puede estar vacío"
        
        return ""
    
    def crear_id(self, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        error = self.validar_crear_editar_id(-1, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas)
        if len(error) > 0:
            return error
        return ""
    
    def validar_crear_editar_id(self, id, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        if nombre_elemento is None or len(nombre_elemento) == 0:
            return "El campo nombre elemento no puede estar vacío"
        
        if numero is None or len(numero) == 0:
            return "El campo número no puede estar vacío"
        
        return ""