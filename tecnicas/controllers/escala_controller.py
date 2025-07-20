from ..models import TipoEscala

class EscalaController():
    def __init__(self):
        pass

    def getTypesScale():
        tipos = TipoEscala.objects.all()
        return tipos
