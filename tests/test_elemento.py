import unittest

from src.logica.Logica import Logica
from src.modelo.elemento import Elemento
from src.modelo.declarative_base import Session
from faker import Faker

class ElementoTestCase(unittest.TestCase):
  def setUp(self):
    self.session = Session()
    self.logica = Logica()
    self.data_factory = Faker()
    Faker.seed(1000)
  
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
                