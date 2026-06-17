# servicios/predictor.py
import joblib
import numpy as np
import os

class Predictor:
    """Encapsula la carga del modelo y la inferencia."""
    
    def __init__(self, ruta_modelo="predictor.joblib"):
        self.ruta_modelo = ruta_modelo
        self.modelo = None
        self._cargar_modelo()
        
    def _cargar_modelo(self):
        # Resolver rutas relativas respecto al archivo actual
        ruta = self.ruta_modelo
        if not os.path.isabs(ruta):
            ruta = os.path.join(os.path.dirname(__file__), ruta)

        try:
            with open(ruta, "rb") as f:
                self.modelo = joblib.load(f)
        except FileNotFoundError:
            raise RuntimeError(f"No se encontró el archivo del modelo en: {ruta}.")
        except Exception as e:
            raise RuntimeError(f"Error cargando el modelo desde {ruta}: {e}")
            
    def predecir(self, vector):
        if self.modelo is None:
            raise RuntimeError("El modelo no esta cargado.")
            
        # pense en pasarlo como un df de pandas pero me daba error, si quieres pruebalo aunque si ya funciona asi, como para que moverle w
        vector_numpy = np.array(vector).reshape(1, -1)
        prediccion = self.modelo.predict(vector_numpy)
        return round(prediccion[0], 2)