import unittest

from src.logica.Logica import Logica
from src.modelo.elemento import Elemento
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.declarative_base import Session
from faker import Faker

class ElementoTestCase(unittest.TestCase):
  def setUp(self):
    self.session = Session()
    self.logica = Logica()
    self.data_factory = Faker()
    Faker.seed(1000)

  def _insertar_clave(self):
    clave = self.data_factory.unique.text()
    nueva_clave = ClaveFavorita(nombre=self.data_factory.unique.name(), clave=clave, pista=clave)
    self.session.add(nueva_clave)
    self.session.commit()

    return nueva_clave
  
  def test_evaluar_elementos_01(self):
    elemento = self.logica.dar_elementos()
    self.assertIsNotNone(elemento)

  def test_evaluar_recuperacion_elemento_agregado_02(self):
    nombre_elemento = self.data_factory.unique.name()
    nuevo_elemento = Elemento(nombreElemento=nombre_elemento, notas=self.data_factory.text())
    self.session.add(nuevo_elemento)
    self.session.commit()
    self.session.close()
    elementos = self.logica.dar_elementos()

    self.assertEquals(elementos[0]['nombre_elemento'], nombre_elemento)

  def test_validar_campos_requeridos_crear_elemento_login_03(self):
    clave = self._insertar_clave()
    nombre = self.data_factory.unique.name()
    email = self.data_factory.unique.email()
    usuario = self.data_factory.unique.name()
    password = clave.nombre
    url = self.data_factory.unique.url()
    notas = self.data_factory.unique.text()

    res = self.logica.crear_login(nombre=None, email=None, usuario=None, password=None, url=None, notas=None)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=nombre, email=None, usuario=None, password=None, url=None, notas=None)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=nombre, email=email, usuario=None, password=None, url=None, notas=None)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=nombre, email=email, usuario=usuario, password=None, url=None, notas=None)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=nombre, email=email, usuario=usuario, password=password, url=None, notas=None)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=nombre, email=email, usuario=usuario, password=password, url=url, notas=None)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=nombre, email=email, usuario=usuario, password=password, url=url, notas=notas)
    self.assertEqual(res, "")

  def test_validar_longitud_campos_requeridos_crear_elemento_login_04(self):
    clave = self._insertar_clave()
    texto_largo = self.data_factory.sentence(300)

    res = self.logica.crear_login(nombre=texto_largo, email=self.data_factory.unique.email(), usuario=texto_largo, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_largo)
    self.assertNotEqual(res, "")

    texto_normal = self.data_factory.text()
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_longitud_notas_crear_elemento_login_05(self):
    clave = self._insertar_clave()
    texto_normal = self.data_factory.text()
    texto_muy_largo = self.data_factory.sentence(600)

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_muy_largo)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_email_crear_elemento_login_06(self):
    clave = self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=texto_normal, usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_url_crear_elemento_login_07(self):
    clave = self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=texto_normal, notas=texto_normal)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_password_crear_elemento_login_08(self):
    clave = self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="", url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_crear_dar_elementos_elemento_login_09(self):
    clave = self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    elementos = self.logica.dar_elementos()

    self.assertEqual(len(elementos), 3)

  def test_validar_nombre_crear_elemento_login_10(self):
    clave = self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    nombre = self.data_factory.unique.name()
    res0 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    res1 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)
    
    nombre = self.data_factory.unique.name()
    res2 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password=clave.nombre, url=self.data_factory.unique.url(), notas=texto_normal)

    self.assertEqual(res0, "")
    self.assertNotEqual(res1, "")
    self.assertEqual(res2, "")

  def test_validar_eliminar_elemento_11(self):
    clave = self._insertar_clave()
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=self.data_factory.text(), password=clave.nombre, url=self.data_factory.unique.url(), notas=self.data_factory.text())
    res = self.logica.dar_elementos()
    self.assertEqual(len(res), 1)

    self.logica.eliminar_elemento(0)
    res = self.logica.dar_elementos()
    self.assertEqual(len(res), 0)
  
  def test_validar_crear_elemento_id_12(self):
    res = self.logica.crear_id(nombre_elemento=None, numero=None, nombre_completo=None, fnacimiento=None, fexpedicion=None, fvencimiento=None, notas=None)
    self.assertNotEqual(res, "")

    nombre_elemento=self.data_factory.unique.name()
    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=None, nombre_completo=None, fnacimiento=None, fexpedicion=None, fvencimiento=None, notas=None)
    self.assertNotEqual(res, "")

    numero=self.data_factory.unique.name()
    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=None, fnacimiento=None, fexpedicion=None, fvencimiento=None, notas=None)
    self.assertNotEqual(res, "")

    nombre_completo=self.data_factory.unique.name()
    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=None, fexpedicion=None, fvencimiento=None, notas=None)
    self.assertNotEqual(res, "")

    fnacimiento=self.data_factory.unique.date()
    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=None, fvencimiento=None, notas=None)
    self.assertNotEqual(res, "")

    fexpedicion=self.data_factory.unique.date()
    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=None, notas=None)
    self.assertNotEqual(res, "")

    fvencimiento=self.data_factory.unique.date()
    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=str(fvencimiento), notas=None)
    self.assertNotEqual(res, "")

    if fexpedicion > fvencimiento:
      aux = fvencimiento
      fvencimiento = fexpedicion
      fexpedicion = aux

    notas=self.data_factory.unique.text()
    texto_largo = self.data_factory.sentence(300)
    res = self.logica.crear_id(nombre_elemento=texto_largo, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=str(fvencimiento), notas=notas)
    self.assertNotEqual(res, "")

    texto_muy_largo = self.data_factory.sentence(600)
    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=str(fvencimiento), notas=texto_muy_largo)
    self.assertNotEqual(res, "")

    texto = self.data_factory.text()
    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=texto, fexpedicion=str(fexpedicion), fvencimiento=str(fvencimiento), notas=notas)
    self.assertNotEqual(res, "")

    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=texto, fvencimiento=str(fvencimiento), notas=notas)
    self.assertNotEqual(res, "")

    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=texto, notas=notas)
    self.assertNotEqual(res, "")

    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fvencimiento), fvencimiento=str(fexpedicion), notas=notas)
    self.assertNotEqual(res, "")

    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=str(fvencimiento), notas=notas)
    self.assertEqual(res, "")

    res = self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=str(fvencimiento), notas=notas)
    self.assertNotEqual(res, "")
  
  def test_validar_editar_elemento_id_13(self):
    nombre_elemento=self.data_factory.unique.name()
    numero=self.data_factory.unique.name()
    nombre_completo=self.data_factory.unique.name()
    fnacimiento=self.data_factory.unique.date()
    fexpedicion=self.data_factory.unique.date()
    fvencimiento=self.data_factory.unique.date()
    if fexpedicion > fvencimiento:
      aux = fvencimiento
      fvencimiento = fexpedicion
      fexpedicion = aux
    notas=self.data_factory.unique.text()

    self.logica.crear_id(nombre_elemento=nombre_elemento, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=str(fvencimiento), notas=notas)
    self.logica.dar_elementos()

    nombre_nuevo=self.data_factory.unique.name()
    numero_nuevo=self.data_factory.unique.name()
    nombre_completo_nuevo=self.data_factory.unique.name()
    fnacimiento_nuevo=self.data_factory.unique.date()
    fexpedicion_nuevo=self.data_factory.unique.date()
    fvencimiento_nuevo=self.data_factory.unique.date()
    if fexpedicion_nuevo > fvencimiento_nuevo:
      aux = fvencimiento_nuevo
      fvencimiento_nuevo = fexpedicion_nuevo
      fexpedicion_nuevo = aux
    notas_nuevo=self.data_factory.unique.text()

    error = self.logica.editar_id(0, nombre_elemento=nombre_nuevo, numero=numero_nuevo, nombre_completo=nombre_completo_nuevo, 
                          fnacimiento=str(fnacimiento_nuevo), fexpedicion=str(fexpedicion_nuevo), 
                          fvencimiento=str(fvencimiento_nuevo), notas=notas_nuevo)
    self.assertEqual(error, "")

    elemento = self.logica.dar_elemento(0)
    self.assertEqual(elemento.nombreElemento, nombre_nuevo)
    self.assertEqual(elemento.numero, numero_nuevo)
    self.assertEqual(elemento.nombre, nombre_completo_nuevo)
    self.assertEqual(elemento['fecha_nacimiento'], str(fnacimiento_nuevo))
    self.assertEqual(elemento['fecha_exp'], str(fexpedicion_nuevo))
    self.assertEqual(elemento['fecha_venc'], str(fvencimiento_nuevo))
    self.assertEqual(elemento.notas, notas_nuevo)

    error = self.logica.editar_id(15, nombre_elemento=nombre_nuevo, numero=numero_nuevo, nombre_completo=nombre_completo_nuevo, 
                          fnacimiento=str(fnacimiento_nuevo), fexpedicion=str(fexpedicion_nuevo), 
                          fvencimiento=str(fvencimiento_nuevo), notas=notas_nuevo)
    self.assertNotEqual(error, "")

    elemento = self.logica.dar_elemento(15)
    self.assertIsNone(elemento)

    nombre_nuevo_2=self.data_factory.unique.name()
    self.logica.crear_id(nombre_elemento=nombre_nuevo_2, numero=numero, nombre_completo=nombre_completo, fnacimiento=str(fnacimiento), fexpedicion=str(fexpedicion), fvencimiento=str(fvencimiento), notas=notas)
    error = self.logica.editar_id(0, nombre_elemento=nombre_nuevo_2, numero=numero_nuevo, nombre_completo=nombre_completo_nuevo, 
                          fnacimiento=str(fnacimiento_nuevo), fexpedicion=str(fexpedicion_nuevo), 
                          fvencimiento=str(fvencimiento_nuevo), notas=notas_nuevo)
    self.assertNotEqual(error, "")
  
  def test_validar_editar_elemento_login_14(self):

    clave = self._insertar_clave()

    nombre_elemento = self.data_factory.unique.name()
    email = self.data_factory.unique.email()
    usuario = self.data_factory.unique.name()
    password = clave.nombre
    url = self.data_factory.unique.url()
    notas = self.data_factory.unique.text()

    self.logica.crear_login(nombre=nombre_elemento, email=email, usuario=usuario, password=password, url=url, notas=notas)
    self.logica.dar_elementos()

    clave_nuevo = self._insertar_clave()
    nombre_elemento_nuevo = self.data_factory.unique.name()
    email_nuevo = self.data_factory.unique.email()
    usuario_nuevo = self.data_factory.unique.name()
    password_nuevo = clave_nuevo.nombre
    url_nuevo = self.data_factory.unique.url()
    notas_nuevo = self.data_factory.unique.text()

    error = self.logica.editar_login(0, nombre=nombre_elemento_nuevo, email=email_nuevo, usuario=usuario_nuevo, password=password_nuevo, url=url_nuevo, notas=notas_nuevo)
    self.assertEqual(error, "")

    elemento = self.logica.dar_elemento(0)
    
    self.assertEqual(elemento.nombreElemento, nombre_elemento_nuevo)
    self.assertEqual(elemento.email, email_nuevo)
    self.assertEqual(elemento.usuario, usuario_nuevo)
    self.assertEqual(elemento.url, url_nuevo)
    self.assertEqual(elemento.notas, notas_nuevo)    

    error = self.logica.editar_login(10, nombre=nombre_elemento_nuevo, email=email_nuevo, usuario=usuario_nuevo, password=password_nuevo, url=url_nuevo, notas=notas_nuevo)
    self.assertNotEqual(error, "")

    elemento = self.logica.dar_elemento(10)
    self.assertIsNone(elemento)

    nombre_nuevo_2=self.data_factory.unique.name()
    self.logica.crear_login(nombre=nombre_nuevo_2, email=email_nuevo, usuario=usuario_nuevo, password=password_nuevo, url=url_nuevo, notas=notas_nuevo)
    error = self.logica.editar_login(0, nombre=nombre_nuevo_2, email=email_nuevo, usuario=usuario_nuevo, password=password_nuevo, url=url_nuevo, notas=notas_nuevo)
    self.assertNotEqual(error, "")