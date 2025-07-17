from models import TipoTecnica, CategoriaTecnica

class TecnicaController():
    def __init__(self):
        pass

    def getTypesTechnique(self):
        tecnias = {"cat1", "cat2", "cat3"}
        categorias = CategoriaTecnica.objects.all()

        for categoria in categorias:
            tipos_tecnica = TipoTecnica.objects.get(pk=categoria.id)

            tecnias = {categoria.nombre_categoria: tipos_tecnica}
            pass

        return tecnias
    
class TiposTecnicas():
    pass