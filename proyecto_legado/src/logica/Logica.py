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
        self.elementos = session.query(Elemento).options(joinedload(Elemento.clave_favorita)).all()
        return self.elementos
    
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
        err = self.validar_crear_editar_login(-1, nombre, email, usuario, password, url, notas)
        if len(err) > 0:
            return err
        
        clave = session.query(ClaveFavorita).filter(ClaveFavorita.nombre == password).first()
        
        nuevo_login = Elemento(tipo=TipoElemento.LOGIN, nombreElemento=nombre, email=email, usuario=usuario, clave_favorita_id=clave.id, url=url, notas=notas)
        session.add(nuevo_login)
        session.commit()

        return ""
    
    def validar_crear_editar_login(self, id, nombre, email, usuario, password, url, notas):

        if id + 1 > len(self.elementos):
            return "El indice es inválido"
        
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
        
        if self.validar_nombre_elemento_duplicado(id, nombre):
            return "Ya existe un elemento con ese nombre"
        
        return ""
    
    def dar_clave(self, nombre_clave):
        clave = session.query(ClaveFavorita).filter(ClaveFavorita.nombre == nombre_clave).first()
        if clave is not None:
            return clave.clave

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
        contar = 0
        hoy = datetime.date.today()

        for elemento in elementos:
            fecha = elemento.fechaVenc
            if fecha is not None:
                anos = fecha.year - hoy.year
                meses = fecha.month - hoy.month 

                if  fecha.day < hoy.day:
                    meses -= 1
                if meses < 0:
                    anos -= 1
                    meses += 12
                diferencia = anos * 12 + meses

                if diferencia < 3:
                    print(elemento.nombreElemento, fecha)
                    contar += 1

        return contar
    
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
        nuevo = Elemento(tipo=TipoElemento.IDENTIFICACION, nombreElemento=nombre_elemento,
                         numero=numero, nombre=nombre_completo, fechaNacimiento=parse(fnacimiento),
                         fechaExp=parse(fexpedicion), fechaVenc=parse(fvencimiento), notas=notas)
        session.add(nuevo)
        session.commit()
        
        return ""

    def editar_id(self, id, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        error = self.validar_crear_editar_id(id, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas)
        if len(error) > 0:
            return error
        
        elemento_existente = self.elementos[id]
            
        elemento_existente.nombreElemento = nombre_elemento
        elemento_existente.numero = numero
        elemento_existente.nombre = nombre_completo
        elemento_existente.fechaNacimiento = parse(fnacimiento)
        elemento_existente.fechaExp = parse(fexpedicion)
        elemento_existente.fechaVenc = parse(fvencimiento)
        elemento_existente.notas = notas
       
        session.commit()

        return ""
    
    def validar_crear_editar_id(self, id, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        if id + 1 > len(self.elementos):
            return "El indice es inválido"
        
        if nombre_elemento is None or len(nombre_elemento) == 0:
            return "El campo nombre elemento no puede estar vacío"
        
        if numero is None or len(numero) == 0:
            return "El campo número no puede estar vacío"
        
        if nombre_completo is None or len(nombre_completo) == 0:
            return "El campo nombre completo no puede estar vacío"
        
        if fnacimiento is None or len(fnacimiento) == 0:
            return "El campo fecha de nacimiento no puede estar vacío"
        
        if fexpedicion is None or len(fexpedicion) == 0:
            return "El campo fecha de expedición no puede estar vacío"
        
        if fvencimiento is None or len(fvencimiento) == 0:
            return "El campo fecha de vencimiento no puede estar vacío"
        
        if notas is None or len(notas) == 0:
            return "El campo notas no puede estar vacío"
        
        if len(nombre_elemento) > 255 or len(numero) > 255 or len(nombre_completo) > 255:
            return "Los campos no puede tener más de 255 caracteres"
        
        if len(notas) > 512:
            return "El campo notas no puede tenes más de 512 caracteres"
        
        try:
            parse(fnacimiento)
        except ValueError:
            return "El campo fecha de nacimiento es inválido"
        datefe = None
        try:
            datefe = parse(fexpedicion)
        except ValueError:
            return "El campo fecha de expedición es inválido"
        datefv = None
        try:
            datefv = parse(fvencimiento)
        except ValueError:
            return "El campo fecha de vencimiento es inválido"
        if  datefv <= datefe:
            return "El campo fecha de expedición debe ser menor a fecha de vencimiento"
        
        if self.validar_nombre_elemento_duplicado(id, nombre_elemento):
            return "Ya existe un elemento con ese nombre"
        
        return ""
    
    def dar_elemento(self, id_elemento):
        if id_elemento + 1 > len(self.elementos):
            return None
        
        return self.elementos[id_elemento]
    
    def validar_nombre_elemento_duplicado(self, id, nombre):
        existe_nombre = session.query(Elemento).filter(Elemento.nombreElemento == nombre).first()

        if id < 0:
            if existe_nombre is None:
                return False
            return True
        
        return existe_nombre and self.elementos[id].id != existe_nombre.id
    
    def editar_login(self, id, nombre, email, usuario, password, url, notas):

        err = self.validar_crear_editar_login(id, nombre, email, usuario, password, url, notas)
        if len(err) > 0:
            return err
        
        clave_favorita = session.query(ClaveFavorita).filter(ClaveFavorita.nombre == password).first()

        elemento_existente = self.elementos[id]            
        elemento_existente.nombreElemento = nombre
        elemento_existente.email = email
        elemento_existente.usuario = usuario
        elemento_existente.clave_favorita_id = clave_favorita.id
        elemento_existente.url = url
        elemento_existente.notas = notas
        
        session.commit()

        return ""

    def eliminar_clave(self, clave_favorita_id):
        try:
            clave_favorita = self.dar_claves_favoritas()[clave_favorita_id]['id']
            dato_clave_favorita = session.query(ClaveFavorita).filter(ClaveFavorita.id == clave_favorita).first()
            elementos = self.dar_elementos()
            
            for elemento in elementos:
                if elemento["clave_favorita_id"] == clave_favorita:
                    return False
            session.delete(dato_clave_favorita)
            session.commit()
            return True
        except:
            return False