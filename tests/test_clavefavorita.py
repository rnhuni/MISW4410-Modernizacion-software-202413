import unittest

from src.logica.Logica import Logica
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.declarative_base import Session

class ClaveFavoritaTestCase(unittest.TestCase):
  def setUp(self):
    self.session = Session()
    self.logica = Logica()
  
  def test_clavefavorita_01(self):
    claves = self.logica.dar_claves_favoritas()
    self.assertIsNot(claves, None)

  def test_clavefavorita_02(self):
    nueva_clave = ClaveFavorita(nombre="Clave de prueba", clave="clave 0", pista="pista 0")
    self.session.add(nueva_clave)
    self.session.commit()
    self.session.close()
    claves = self.logica.dar_claves_favoritas()

    self.assertEquals(claves[0]['nombre'], "Clave de prueba")