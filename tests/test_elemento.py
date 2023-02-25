import unittest

from src.logica.Logica import Logica
from src.modelo.clave_favorita import Elemento
from src.modelo.declarative_base import Session

class ElementoTestCase(unittest.TestCase):
  def setUp(self):
    self.session = Session()
    self.logica = Logica()
  
  def test_elemento_01(self):
    elemento = self.logica.dar_elementos()
    self.assertIsNotNone(elemento)

  def test_elemento_02(self):
    nuevo_elemento = Elemento(nombreElemento="Elemento de prueba", notas="Nota 0", claveFavorita=None)
    self.session.add(nuevo_elemento)
    self.session.commit()
    self.session.close()
    elementos = self.logica.dar_elementos()

    self.assertEquals(elementos[0]['nombreElemento'], "Elemento de prueba")
                