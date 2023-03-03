import unittest

from src.logica.Logica import Logica
from src.modelo.elemento import Elemento, TipoElemento
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.declarative_base import Session
from faker import Faker

class ReporteTestCase(unittest.TestCase):
  def setUp(self):
    self.logica = Logica()
    self.data_factory = Faker()
    Faker.seed(1000)
  
  def test_evaluar_contarclavesinseguras_01(self):
    claves = []
    clave = self.logica.generar_clave()
    claves.append(ClaveFavorita(clave=clave))
    clave = self.logica.generar_clave()
    claves.append(ClaveFavorita(clave=clave))
    clave = self.logica.generar_clave()
    claves.append(ClaveFavorita(clave=clave))
    clave = self.data_factory.unique.text()
    claves.append(ClaveFavorita(clave=clave))

    self.assertEqual(self.logica.contar_claves_inseguras(claves), 3)

  