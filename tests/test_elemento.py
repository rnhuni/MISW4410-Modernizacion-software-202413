import unittest

from src.logica.Logica import Logica

class ElementoTestCase(unittest.TestCase):
  def setUp(self):
    self.logica = Logica()
  
  def test_elemento_01(self):
    elemento = self.logica.dar_elementos()
    self.assertIsNotNone(elemento)
                