from ..models import TipoTecnica, CategoriaTecnica, Tecnica, EstiloPalabra
from django.db import DatabaseError
from ..utils import controller_error


class TecnicaController():
    def setTechnique(self, **kwargs):
        self.technique = Tecnica(
            tipo_tecnica=kwargs["tipo_tecnica"],
            id_estilo=kwargs["estilo_palabras"],
            repeticiones_max=kwargs["numero_repeticiones"] or 0,
            limite_catadores=kwargs["numero_catadores"],
            instrucciones=kwargs["instrucciones"],
        )

    def setTechniqueFromBasicData(self, basic):
        self.technique = Tecnica(
            tipo_tecnica=TipoTecnica.objects.get(id=basic["id_tecnica"]),
            id_estilo=EstiloPalabra.objects.get(id=basic["estilo_palabras"]),
            repeticiones_max=basic["numero_repeticiones"] or 0,
            limite_catadores=basic["numero_catadores"],
            instrucciones=basic["instrucciones"] or "Espere instrucciones del Presentador",
        )

    def getDataTechnique(self):
        return self.technique.toDict()

    def saveTechnique(self):
        try:
            self.technique.save()
            return self.technique
        except DatabaseError:
            return controller_error("No se ha podido guardar la tecnica")

    def deleteTechnique(self):
        self.technique.delete()

    @staticmethod
    def getTechniqueById(id: int):
        try:
            technique = Tecnica.objects.get(id)
            return technique
        except Tecnica.DoesNotExist:
            return controller_error("Técnica no encontrada")

    @staticmethod
    def getTypesTechnique():
        showTecnicas = {}
        categories = CategoriaTecnica.objects.all()

        for cata in categories:
            tecnicas = TipoTecnica.objects.filter(id_categoria_tecnica=cata.id)
            showTecnicas[cata.nombre_categoria] = tecnicas

        return showTecnicas
