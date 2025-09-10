from ..models import Etiqueta, EtiquetasEscala, Escala, TipoEscala
from django.db import DatabaseError
from ..utils import controller_error


class EscalaController():
    scale: Escala
    tags_relation: dict[str, EtiquetasEscala]

    def __init__(self, data):
        self.scale = Escala(
            id_tipo_escala=TipoEscala.objects.get(id=data["id_scale"]),
            longitud=data["size"],
            tecnica=data["technique"]
        )

    def setScale(self, newData):
        self.scale = Escala(
            id_tipo_escala=TipoEscala.objects.get(id=newData["id_scale"]),
            longitud=newData["size"],
            tecnica=newData["technique"]
        )

    def saveScale(self):
        try:
            self.scale.save()
            return self.scale
        except DatabaseError as error:
            return controller_error("error al guardar la escala")

    def deleteScale(self):
        self.scale.delete()

    def addAndSaveTags(self, tags: dict):
        self.tags_relation = {}
        if self.scale.id_tipo_escala.nombre_escala == "cotinua":
            ok_tags = self.realte_tags_type_cotinue(tags)
            if ok_tags["error"]:
                return ok_tags
            return self.tags_relation

        elif self.scale.id_tipo_escala.nombre_escala == "estructurada":
            ok_tags = self.realte_tags_type_structure(tags)
            if ok_tags["error"]:
                return ok_tags
            return self.tags_relation

    def deleteRelationshipsWithLabels(self):
        for name, tag in self.tags_relation.items():
            tag.delete()

    def realteTags(self, tags: dict):
        try:
            index = 1
            self.tags_relation = {}

            for name, id_tag in tags.items():
                tag = Etiqueta.objects.get(id=id_tag)
                related_tag = EtiquetasEscala.objects.create(
                    id_escala=self.scale,
                    id_etiqueta=tag,
                    posicion=index
                )
                self.tags_relation[name] = related_tag
                index += 1

            return self.tags_relation
        except DatabaseError as error:
            self.deleteRelationshipsWithLabels()
            return controller_error("error guardar relacion etiqueta escala")
