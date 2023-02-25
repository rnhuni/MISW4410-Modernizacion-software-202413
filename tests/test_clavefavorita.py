import unittest

from src.logica.Logica import Logica

class ClaveFavoritaTestCase(unittest.TestCase):
  def setUp(self):
    self.logica = Logica()
  
  def test_clavefavorita_01(self):
    claves = self.logica.dar_claves_favoritas()
    self.assertIsNot(claves, None)