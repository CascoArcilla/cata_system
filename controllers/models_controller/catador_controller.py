from tecnicas.models import Catador
from utils import controller_error

class CatadorController:
    def getTesterByUsername(username:str):
        try:
            tester = Catador.objects.get(usuarioCatador=username)
            return tester
        except Catador.DoesNotExist:
            return controller_error("No se encontró el Catador")
