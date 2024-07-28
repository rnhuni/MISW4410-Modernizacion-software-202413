from flask import request, make_response
from flask_restful import Resource

class VistaClaveFavorita(Resource):
    def __init__(self, logica):
        self.logica = logica
    
    def post(self):
        nombre = request.json.get('nombre')
        clave = request.json.get('clave')
        pista = request.json.get('pista')
        clavedb = self.logica.crear_clave(nombre, clave, pista)

        if isinstance(clavedb, str):
            return {"error": clavedb}, 400
        
        return clavedb.id, 201
    
    def get(self):
        claves_favoritas = self.logica.dar_claves_favoritas()
        claves_favoritas_list = [self.clave_to_dict(clave) for clave in claves_favoritas]

        return claves_favoritas_list, 200
    
    def clave_to_dict(self, clave):
        return {
            'id': clave.id,
            'nombre': clave.nombre,
            'clave': clave.clave,
            'pista': clave.pista
        }
