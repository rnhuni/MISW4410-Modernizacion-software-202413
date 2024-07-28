import unittest

from src.logica.Logica import Logica

class ClaveMaestraTestCase(unittest.TestCase):
  def setUp(self):
    self.logica = Logica()
  
  def test_evaluar_clavemaestra_01(self):
    claveMaestra = self.logica.dar_claveMaestra()
    self.assertIsInstance(claveMaestra, str)

  def test_evaluar_clavemaestra_02(self):
    claveMaestra = self.logica.dar_claveMaestra()
    self.assertGreater(len(claveMaestra), 0)
                