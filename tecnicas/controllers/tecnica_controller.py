from ..models import TipoTecnica, CategoriaTecnica

class TecnicaController():
    def __init__(self):
        pass

    @staticmethod
    def getTypesTechnique():
        showTecnicas = {}
        categorias = CategoriaTecnica.objects.all()

        # for categoria in categorias:
        #     tipos_tecnica = TipoTecnica.objects.get(pk=categoria.id)

        #     tecnias = {categoria.nombre_categoria: tipos_tecnica}
        #     pass

        for cata in categorias:
            tecnicas = TipoTecnica.objects.filter(id_categoria_tecnica=cata.id)
            showTecnicas[cata.nombre_categoria] = tecnicas

        return showTecnicas