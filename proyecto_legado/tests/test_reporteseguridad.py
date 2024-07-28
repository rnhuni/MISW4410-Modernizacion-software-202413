import unittest

from src.logica.Logica import Logica
from src.modelo.elemento import Elemento, TipoElemento
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.declarative_base import Session
from faker import Faker

class ReporteTestCase(unittest.TestCase):
  def setUp(self):
    self.session = Session()
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

    self.assertEqual(self.logica.contar_claves_inseguras(claves), 1)

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

  def test_evaluar_calcularr_03(self):
    elementos = []
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))

    r1 = self.logica.calcular_r(elementos)

    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))

    r05_1 = self.logica.calcular_r(elementos)

    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))

    r05_2 = self.logica.calcular_r(elementos)

    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))
    elementos.append(Elemento(clave_favorita_id=clave_favorita_id))

    r0 = self.logica.calcular_r(elementos)

    self.assertEqual(r1, 1.0)
    self.assertEqual(r05_1, 0.5)
    self.assertEqual(r05_2, 0.5)
    self.assertEqual(r0, 0.0)

  def test_calculo_nivel_seguridad_04(self):
    nivel_1 = self.logica.calcular_nivel_seguridad(10, 5, 20, 0, 1)
    nivel_2 = self.logica.calcular_nivel_seguridad(20, 7, 8, 0, 0.5)
    nivel_3 = self.logica.calcular_nivel_seguridad(12, 3, 6, 0, 0)
    self.assertEqual(nivel_1, 2.1)
    self.assertEqual(nivel_2, 3.378)
    self.assertEqual(nivel_3, 1.6520000000000001)
  
  def test_evaluar_reporteseguridad_05(self):
    elementos = []
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.LOGIN))
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.LOGIN))
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.SECRETO))
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.SECRETO))
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.TARJETA))
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.TARJETA))
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.TARJETA))
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.TARJETA))
    clave_favorita_id = self.data_factory.random_int(1, 10000)
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.IDENTIFICACION))
    self.session.add(Elemento(clave_favorita_id=clave_favorita_id, tipo=TipoElemento.IDENTIFICACION))
    claves = []
    clave = self.logica.generar_clave()
    self.session.add(ClaveFavorita(clave=clave))
    clave = self.logica.generar_clave()
    self.session.add(ClaveFavorita(clave=clave))
    clave = self.logica.generar_clave()
    self.session.add(ClaveFavorita(clave=clave))
    clave = self.data_factory.unique.text()
    self.session.add(ClaveFavorita(clave=clave))
    self.session.commit()
    self.session.close()
    datos_reporte = self.logica.dar_reporte_seguridad()
    self.assertEqual(datos_reporte['logins'], 2)
    self.assertEqual(datos_reporte['ids'], 2)
    self.assertEqual(datos_reporte['tarjetas'], 4)
    self.assertEqual(datos_reporte['secretos'], 2)
    self.assertEqual(datos_reporte['inseguras'], 1)
    self.assertEqual(datos_reporte['avencer'], 0)
    self.assertEqual(datos_reporte['masdeuna'], 4)
    self.assertEqual(datos_reporte['nivel'], 0.8200000000000001)