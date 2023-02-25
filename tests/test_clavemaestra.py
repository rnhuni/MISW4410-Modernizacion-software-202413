import unittest

from src.logica.Logica import Logica

class ClaveMaestraTestCase(unittest.TestCase):
  def setUp(self):
    self.logica = Logica()
  
  def test_clavemaestra_01(self):
    claveMaestra = self.logica.dar_claveMaestra()
    self.assertIsInstance(claveMaestra, str)
                