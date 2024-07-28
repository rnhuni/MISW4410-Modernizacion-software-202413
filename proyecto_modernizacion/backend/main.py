import os
from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from src.vista.VistaClave import VistaClaveFavorita
from src.vista.VistaHealthCheck import VistaHealthCheck
from src.logica.Logica import Logica

app = Flask(__name__)

cors = CORS(app)
api = Api(app)

logica_negocio = Logica()

api.add_resource(VistaClaveFavorita, '/clave-favorita', resource_class_kwargs={'logica': logica_negocio})
api.add_resource(VistaHealthCheck, '/')

if __name__ == '__main__':
    app.run(debug=True)
