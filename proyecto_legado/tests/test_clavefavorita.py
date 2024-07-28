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
  
  def _dar_clave_id(self, claves, nombre_clave):
    for index, clave in enumerate(claves):
      if clave.nombre == nombre_clave:
        return  index
    return -1
        
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
    clave = self.data_factory.unique.name()
    pista = self.data_factory.unique.name()
    
    crear_respuesta = self.logica.crear_clave(nombre=None, clave=None, pista=None)
    self.assertNotEqual(crear_respuesta, '')

    crear_respuesta = self.logica.crear_clave(nombre=nombre_clave, clave=None, pista=None)
    self.assertNotEqual(crear_respuesta, '')

    crear_respuesta = self.logica.crear_clave(nombre=nombre_clave, clave=clave, pista=None)
    self.assertNotEqual(crear_respuesta, '')

    crear_respuesta = self.logica.crear_clave(nombre=nombre_clave, clave=clave, pista=pista)
    self.assertEqual(crear_respuesta, '')

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
    nombre_aleatorio = self.data_factory.unique.name()
    clave_aleatoria = self.data_factory.unique.text()
    self.logica.crear_clave(nombre=nombre_aleatorio, clave=clave_aleatoria, pista=clave_aleatoria)

    claves = self.logica.dar_claves_favoritas()
    exists = False
    for clave in claves:
      if clave["nombre"] == nombre_aleatorio:
        exists = True
        break

    self.assertEqual(exists, True)
  
  def test_valida_clave_no_este_almacenada_con_mismo_nombre_08(self):
    nombre_aleatorio = self.data_factory.unique.name()
    clave_aleatoria = self.data_factory.unique.text()
    self.logica.crear_clave(nombre=nombre_aleatorio, clave=clave_aleatoria, pista=clave_aleatoria)
    resultado = self.logica.crear_clave(nombre=nombre_aleatorio, clave=clave_aleatoria, pista=clave_aleatoria)    
    self.assertNotEqual(resultado, '')

    resultado = self.logica.crear_clave(nombre=self.data_factory.unique.name(), clave=clave_aleatoria, pista=clave_aleatoria)    
    self.assertEqual(resultado, '')

  def test_valida_que_clave_exista_09(self):
    nombre_aleatorio = self.data_factory.unique.name()
    nombre_aleatorio_sin_insertar = self.data_factory.unique.name()
    clave_aleatoria = self.data_factory.unique.name()
    error = self.logica.crear_clave(nombre=nombre_aleatorio, clave=clave_aleatoria, pista=clave_aleatoria)
    self.assertEqual(error, "")

    respuesta = self.logica.dar_clave(nombre_aleatorio_sin_insertar)
    self.assertIsNone(respuesta)

    respuesta = self.logica.dar_clave(nombre_aleatorio)
    self.assertIsNotNone(respuesta)
    
  
  def test_valida_campos_requeridos_editar_clave_10(self):
    nombre_clave_1 = self.data_factory.unique.name()
    nombre_clave_1_nuevo = self.data_factory.unique.name()
    nombre_clave_2 = self.data_factory.unique.name()
    clave = self.data_factory.unique.name()
    pista = self.data_factory.unique.name()

    self.logica.crear_clave(nombre=nombre_clave_1, clave=clave, pista=pista)
    self.logica.crear_clave(nombre=nombre_clave_2, clave=clave, pista=pista)
    self.logica.dar_claves_favoritas()

    respuesta = self.logica.editar_clave(id=None, nombre=None, clave=None, pista=None)
    self.assertNotEqual(respuesta, '')

    respuesta = self.logica.editar_clave(id=1, nombre=None, clave=None, pista=None)
    self.assertNotEqual(respuesta, '')

    respuesta = self.logica.editar_clave(id=1, nombre=nombre_clave_1, clave=None, pista=None)
    self.assertNotEqual(respuesta, '')

    respuesta = self.logica.editar_clave(id=1, nombre=nombre_clave_1, clave=clave, pista=None)
    self.assertNotEqual(respuesta, '')

    respuesta = self.logica.editar_clave(id=1, nombre=nombre_clave_1_nuevo, clave=clave, pista=pista)
    self.assertEqual(respuesta, '')
  
  def test_valida_nombre_duplicado_editar_clave_11(self):
    nombre_aleatorio = self.data_factory.unique.name()
    nombre_aleatorio_nuevo = self.data_factory.unique.name()
    nombre_aleatorio_dos = nombre_aleatorio + ' 2';
    clave_aleatoria = self.data_factory.unique.text()
    clave_aleatoria_dos = self.data_factory.unique.text()
    self.logica.crear_clave(nombre=nombre_aleatorio, clave=clave_aleatoria, pista=clave_aleatoria)
    self.logica.crear_clave(nombre=nombre_aleatorio_dos, clave=clave_aleatoria_dos, pista=clave_aleatoria_dos)
    self.logica.dar_claves_favoritas()

    respuesta = self.logica.editar_clave(id=1, nombre=nombre_aleatorio, clave=clave_aleatoria_dos, pista=clave_aleatoria_dos)
    self.assertNotEqual(respuesta, "")

    respuesta = self.logica.editar_clave(id=1, nombre=nombre_aleatorio_nuevo, clave=clave_aleatoria_dos, pista=clave_aleatoria_dos)
    self.assertEqual(respuesta, "")

    respuesta = self.logica.editar_clave(id=1, nombre=nombre_aleatorio_nuevo, clave=clave_aleatoria_dos, pista=self.data_factory.unique.text())
    self.assertEqual(respuesta, "")

  def test_validar_clave_favorita_en_elemento_12(self):
    nombre_clave = self.data_factory.unique.name()
    nombre_clave_2 = self.data_factory.unique.name()
    clave = self.data_factory.unique.password(special_chars=False)
    self.logica.crear_clave(nombre=nombre_clave, clave=clave, pista=clave)
    
    self.logica.crear_clave(nombre=nombre_clave_2, clave=clave, pista=clave)
    claves = self.logica.dar_claves_favoritas()
    consulta = self._dar_clave_id(claves, nombre_clave_2)
    respuesta = self.logica.eliminar_clave(consulta)
    self.assertEqual(respuesta, True)
    
    texto_normal = self.data_factory.text()
    error = self.logica.crear_login(nombre=self.data_factory.unique.name(), email=self.data_factory.unique.email(), usuario=self.data_factory.unique.name(), password=nombre_clave, url=self.data_factory.unique.url(), notas=texto_normal)
    self.assertEqual(error, "")

    claves = self.logica.dar_claves_favoritas()
    self.logica.dar_elementos()
    consulta = self._dar_clave_id(claves, nombre_clave)
    respuesta = self.logica.eliminar_clave(consulta)
    self.assertEqual(respuesta, False)

    nombre_clave_nuevo = self.data_factory.unique.name()
    clave_nuevo = self.data_factory.unique.password(special_chars=False)
    self.logica.crear_clave(nombre=nombre_clave_nuevo, clave=clave_nuevo, pista=clave_nuevo)

    respuesta = self.logica.eliminar_clave(15)
    self.assertEqual(respuesta, False)

    claves = self.logica.dar_claves_favoritas()
    consulta = self._dar_clave_id(claves, nombre_clave_nuevo)
    respuesta = self.logica.eliminar_clave(consulta)

    self.assertEqual(respuesta, True)