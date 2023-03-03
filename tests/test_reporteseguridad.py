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

  def test_evaluar_calcularmasdeuna_02(self):
    elementos = []
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))

    self.assertEqual(self.logica.calcular_masdeuna(elementos), 4)