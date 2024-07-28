import sys
from src.vista.InterfazCajaSeguridad import App_CajaDeSeguridad
from src.logica.Logica import Logica

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = Logica()

    app = App_CajaDeSeguridad(sys.argv, logica)
    sys.exit(app.exec_())