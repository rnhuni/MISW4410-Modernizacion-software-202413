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

    self.assertEquals(elementos[0]['nombreElemento'], nombre_elemento)

  def test_validar_campos_requeridos_crear_elemento_login_03(self):
    res = self.logica.crear_login(nombre=None, email=None, usuario=None, password=None, url=None, notas=None)
    self.assertEqual(res, False)

  def test_validar_longitud_campos_requeridos_crear_elemento_login_04(self):
    self._insertar_clave()
    texto_largo = self.data_factory.sentence(300)

    res = self.logica.crear_login(nombre=texto_largo, email=self.data_factory.unique.email(), usuario=texto_largo, password=1, url=self.data_factory.unique.url(), notas=texto_largo)
    self.assertEqual(res, False)

    texto_normal = self.data_factory.text()
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, True)

  def test_validar_longitud_notas_crear_elemento_login_05(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    texto_muy_largo = self.data_factory.sentence(600)

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_muy_largo)
    self.assertEqual(res, False)

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, True)

  def test_validar_email_crear_elemento_login_06(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=texto_normal, usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, False)

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, True)

  def test_validar_url_crear_elemento_login_07(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=texto_normal, notas=texto_normal)
    self.assertEqual(res, False)

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, True)

  def test_validar_password_crear_elemento_login_08(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=0, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, False)

    res = self.logica.crear_login(nombre=texto_normal, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(res, True)

  def test_validar_crear_dar_elementos_elemento_login_09(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    elementos = self.logica.dar_elementos()

    self.assertEqual(len(elementos), 3)

  def test_validar_nombre_crear_elemento_login_10(self):
    self._insertar_clave()
    texto_normal = self.data_factory.text()
    
    nombre = self.data_factory.unique.name()
    res0 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    res1 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)
    
    nombre = self.data_factory.unique.name()
    res2 = self.logica.crear_login(nombre=nombre, email=self.data_factory.unique.email(), usuario=texto_normal, password=1, url=self.data_factory.unique.url(), notas=texto_normal)

    self.assertEqual(res0, True)
    self.assertEqual(res1, False)
    self.assertEqual(res2, True)