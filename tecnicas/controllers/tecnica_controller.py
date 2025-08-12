from ..models import TipoTecnica, CategoriaTecnica, Tecnica


class TecnicaController():
    def setTechnique(self, **kwargs):
        self.technique = Tecnica.objects.create(
            tipo_tecnica=kwargs["tipo_tecnica"],
            repeticiones_max=kwargs["numero_repeticiones"] or 0,
            limite_catadores=kwargs["numero_catadores"],
            instrucciones=kwargs["instrucciones"],
            id_estilo=kwargs["estilo_palabras"],
        )

    @staticmethod
    def getTypesTechnique():
        showTecnicas = {}
        categories = CategoriaTecnica.objects.all()

        for cata in categories:
            tecnicas = TipoTecnica.objects.filter(id_categoria_tecnica=cata.id)
            showTecnicas[cata.nombre_categoria] = tecnicas

        return showTecnicas
