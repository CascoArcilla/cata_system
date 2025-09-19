from ..models import Presentador
from ..utils import controller_error


class PresentadorController():
    def __init__(self):
        pass

    @staticmethod
    def getPresenterByUsername(username: str):
        try:
            presenter = Presentador.objects.get(nombre_usuario=username)
        except Presentador.DoesNotExist:
            return controller_error("Presentador inexistente")
