from ..models import Etiqueta, EtiquetasEscala, Escala
from django.db import DatabaseError


class EscalaController():
    scale: Escala
    tags: list[tuple[str, EtiquetasEscala]]

    def __init__(self, data):
        self.scale = Escala(
            id_tipo_escala=data["scale"],
            longitud=data["size"],
            tecnica=data["technique"]
        )

    def setScale(self, newData):
        self.scale = Escala(
            id_tipo_escala=newData["scale"],
            longitud=newData["size"],
            tecnica=newData["technique"]
        )

    def saveScale(self):
        try:
            self.scale.save()
        except Exception:
            return False
        return self.scale

    def deleteScale(self):
        self.scale.delete()

    def addAndSaveTags(self, tags: list):
        if self.scale.id_tipo_escala.nombre_escala == "cotinua":
            if not self.realte_tags_type_cotinue(tags):
                return False
        elif self.scale.id_tipo_escala.nombre_escala == "estructurada":
            if not self.realte_tags_type_structure(tags):
                return False
        return self.tags

    def deleteRelationshipsWithLabels(self):
        for tuple in self.tags:
            relaTag = tuple[1]
            relaTag.adelete()

    def realte_tags_type_cotinue(self, tags: list):
        try:
            tag_start = Etiqueta.objects.get(id=tags["punto_inicial"])
            start_point = EtiquetasEscala.objects.create(
                id_escala=self.scale.id,
                id_etiqueta=tag_start,
                posicion=1
            )

            self.tags.append(("start", start_point))

            tag_medium = Etiqueta.objects.get(id=tags["punto_medio"])
            half_point = EtiquetasEscala.objects.create(
                id_escala=self.scale.id,
                id_etiqueta=tag_medium,
                posicion=2
            )

            self.tags.append(("medium", half_point))

            tag_end = Etiqueta.objects.get(id=tags["punto_final"])
            end_point = EtiquetasEscala.objects.create(
                id_escala=self.scale.id,
                id_etiqueta=tag_end,
                posicion=3
            )

            self.tags.append(("end", end_point))
            return True
        except DatabaseError as error:
            self.deleteRelationshipsWithLabels()
            return False

    def realte_tags_type_structure(self, tags: dict):
        try:
            index = 1
            self.tags = []

            for name, id_tag in tags.items():
                tag = Etiqueta.objects.get(id=id_tag)
                related_tag = EtiquetasEscala(
                    id_escala=self.scale.id,
                    id_etiqueta=tag,
                    posicion=index
                )
                self.tags.append((name, related_tag))
                index += 1

            return True
        except DatabaseError as error:
            self.deleteRelationshipsWithLabels()
            return False
