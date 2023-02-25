from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad

class Logica(FachadaCajaDeSeguridad):
    
    def __init__(self):
        self.clave_maestra = 'clave'

    def dar_claveMaestra(self):
        return self.clave_maestra
    
    def dar_claves_favoritas(self):
        return None
    
    def crear_clave(self, nombre, clave, pista):
        return None
    
    def generar_clave(self):
        return None
    
    def dar_elementos(self):
        return None
    