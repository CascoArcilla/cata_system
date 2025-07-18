from ..models import TipoTecnica, CategoriaTecnica

class TecnicaController():
    def __init__(self):
        pass

    @staticmethod
    def getTypesTechnique():
        showTecnicas = {}
        categorias = CategoriaTecnica.objects.all()

        for cata in categorias:
            tecnicas = TipoTecnica.objects.filter(id_categoria_tecnica=cata.id)
            showTecnicas[cata.nombre_categoria] = tecnicas

        return showTecnicas