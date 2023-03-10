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
    self.session.close()
  
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
    nombre = self.data_factory.unique.name()
    email = self.data_factory.unique.email()
    usuario = self.data_factory.unique.name()
    password = self.data_factory.unique.name()
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
    self._insertar_clave()
    texto_largo = self.data_factory.sentence(300)

    res = self.logica.crear_login(nombre=texto_largo, email=self.data_factory.unique.email(), usuario=texto_largo, password="1", url=self.data_factory.unique.url(), notas=texto_largo)
    self.assertNotEqual(res, "")

    texto_normal = self.data_factory.text()
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_longitud_notas_crear_elemento_login_05(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    texto_muy_largo = self.data_factory.sentence(600)

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_muy_largo)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_email_crear_elemento_login_06(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=texto_normal, usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_url_crear_elemento_login_07(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=texto_normal, notas=texto_normal)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_password_crear_elemento_login_08(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="", url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertNotEqual(res, "")

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, "")

  def test_validar_crear_dar_elementos_elemento_login_09(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    elementos = self.logica.dar_elementos()

    self.assertEqual(len(elementos), 3)

  def test_validar_nombre_crear_elemento_login_10(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    nombre = self.data_factory.unique.name()
    res0 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    res1 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)
    
    nombre = self.data_factory.unique.name()
    res2 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password="1", url=self.data_factory.unique.url(), notas=texto_normal)

    self.assertEqual(res0, "")
    self.assertNotEqual(res1, "")
    self.assertEqual(res2, "")

  def test_validar_eliminar_elemento_11(self):
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=self.data_factory.text(), password="1", url=self.data_factory.unique.url(), notas=self.data_factory.text())
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