from ...models import Etiqueta, EtiquetasEscala, Escala, TipoEscala, Tecnica
from django.db import DatabaseError
from ...utils import controller_error


class EscalaController():
    scale: Escala
    tags_relation: dict[str, EtiquetasEscala]

    def __init__(self, data, use_scale: Escala = None):
        if use_scale:
            self.scale = use_scale
        else:
            self.scale = Escala(
                id_tipo_escala=TipoEscala.objects.get(id=data["id_scale"]),
                longitud=data["size"],
                tecnica=data["technique"]
            )

    def setScale(self, newData, use_scale: Escala):
        if use_scale:
            self.scale = use_scale
        else:
            self.scale = Escala(
                id_tipo_escala=TipoEscala.objects.get(id=data["id_scale"]),
                longitud=data["size"],
                tecnica=data["technique"]
            )

    def saveScale(self):
        try:
            self.scale.save()
            return self.scale
        except DatabaseError as error:
            return controller_error("Error al guardar la escala")

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
            return controller_error("Error en guardar la relación etiqueta escala")

    @staticmethod
    def getScaleByTechnique(technique: Tecnica = None, id_technique: int = None):
        if technique is not None:
            scale = Escala.objects.select_related("id_tipo_escala").only(
                "id_tipo_escala", "longitud").get(tecnica=technique)
            return scale

        if id_technique is not None:
            scale = Escala.objects.select_related("id_tipo_escala").only(
                "id_tipo_escala", "longitud").get(tecnica_id=id_technique)
            return scale

    @staticmethod
    def getRelatedTagsInScale(scale: Escala = None, id_scale: int = None):
        if scale is not None:
            scale_tags = list(EtiquetasEscala.objects.filter(
                id_escala=scale).select_related("id_etiqueta"))
            if len(scale_tags) == 0:
                return controller_error("Imposible obtener las etiquetas")
            return scale_tags

        if id_scale is not None:
            scale_tags = list(EtiquetasEscala.objects.filter(
                id_escala_id=scale).select_related("id_etiqueta"))
            if len(scale_tags) == 0:
                return controller_error("Imposible obtener las etiquetas")
            return scale_tags
