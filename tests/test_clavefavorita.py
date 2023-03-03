import unittest

from src.logica.Logica import Logica
from src.modelo.clave_favorita import ClaveFavorita
from src.modelo.declarative_base import Session
from faker import Faker

class ClaveFavoritaTestCase(unittest.TestCase):
  def setUp(self):
    self.session = Session()
    self.logica = Logica()
    self.data_factory = Faker()
    Faker.seed(1000)
  
  def test_evaluar_clavesfavoritas_01(self):
    claves = self.logica.dar_claves_favoritas()
    self.assertIsNot(claves, None)

  def test_evaluar_recuperacion_clavefavorita_agregada_02(self):
    nombre_clave = self.data_factory.unique.name()
    clave = self.data_factory.text()
    nueva_clave = ClaveFavorita(nombre=nombre_clave, clave=clave, pista=clave)
    self.session.add(nueva_clave)
    self.session.commit()
    self.session.close()
    claves = self.logica.dar_claves_favoritas()

    self.assertEqual(claves[0]['nombre'], nombre_clave)

  def test_evaluar_declaracion_campos_clavefavorita_03(self):
    nombre_clave = self.data_factory.unique.name()
    crear_respuesta = self.logica.crear_clave(nombre=nombre_clave, clave=None, pista=None)
    self.assertEqual(crear_respuesta, False)
  
  def test_valida_pista_clave_iguales_04(self):
    crear_respuesta = self.logica.crear_clave(nombre="Clave de prueba", clave="clave", pista="prueba")
    self.assertEqual(crear_respuesta, False)

  def test_valida_clave_si_es_segura_05(self):
    respuesta = self.logica.es_clave_segura("clave123")
    self.assertEqual(respuesta, False)

    respuesta = self.logica.es_clave_segura("Clav3S3gura*_")
    self.assertEqual(respuesta, True)
  
  def test_valida_clave_generada_si_es_segura_06(self):
    respuesta_generar = self.logica.generar_clave()
    respuesta = self.logica.es_clave_segura(respuesta_generar)
    self.assertEqual(respuesta, True)

  def test_valida_guardar_clave_y_se_visualiza_en_dar_claves_favoritas_07(self):
    self.logica.crear_clave(nombre="Ultima clave", clave='S3gura', pista='S3gura')
    claves = self.logica.dar_claves_favoritas()
    exists = False
    for clave in claves:
      if clave["nombre"] == "Ultima clave":
        exists = True
        break
    self.assertEqual(exists, True)
  
  def test_valida_clave_no_este_almacenada_con_mismo_nombre_08(self):
    self.logica.crear_clave(nombre="Ultima clave repetida", clave='S3gura*', pista='S3gura*')
    resultado = self.logica.crear_clave(nombre="Ultima clave repetida", clave='S3gura*', pista='S3gura*')    
    self.assertEqual(resultado, False)