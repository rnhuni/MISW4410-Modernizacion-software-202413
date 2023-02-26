import unittest

from src.logica.Logica import Logica
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.declarative_base import Session

class ClaveFavoritaTestCase(unittest.TestCase):
  def setUp(self):
    self.session = Session()
    self.logica = Logica()
  
  """ def test_clavefavorita_01(self):
    claves = self.logica.dar_claves_favoritas()
    self.assertIsNot(claves, None)

  def test_clavefavorita_02(self):
    nueva_clave = ClaveFavorita(nombre="Clave de prueba", clave="clave 0", pista="pista 0")
    self.session.add(nueva_clave)
    self.session.commit()
    self.session.close()
    claves = self.logica.dar_claves_favoritas()

    self.assertEqual(claves[0]['nombre'], "Clave de prueba")

  def test_clavefavorita_03(self):
    crear_respuesta = self.logica.crear_clave(nombre="Clave de prueba", clave=None, pista=None)
    self.assertEqual(crear_respuesta, False)
  
  def test_clavefavorita_04(self):
    crear_respuesta = self.logica.crear_clave(nombre="Clave de prueba", clave="clave", pista="prueba")
    self.assertEqual(crear_respuesta, False)

  def test_clavefavorita_05(self):
    respuesta = self.logica.es_clave_segura("clave123")
    self.assertEqual(respuesta, False)

    respuesta = self.logica.es_clave_segura("Clav3S3gura*_")
    self.assertEqual(respuesta, True)
  
  def test_clavefavorita_06(self):
    respuesta_generar = self.logica.generar_clave()
    respuesta = self.logica.es_clave_segura(respuesta_generar)
    self.assertEqual(respuesta, True) """

  def test_clavefavorita_07(self):

    nueva_clave = ClaveFavorita(nombre="Clave de prueba 11", clave="clave 0", pista="pista 0")
    self.session.add(nueva_clave)
    self.session.commit()
    self.session.close()

    claves = self.logica.dar_claves_favoritas()
    print(claves[len(claves) -1]['nombre'])