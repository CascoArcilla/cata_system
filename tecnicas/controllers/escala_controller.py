from ..models import TipoEscala, Etiqueta, EtiquetasEscala, Escala, Tecnica


class EscalaController():

    scale: Escala

    def __init__(self, scale):
        self.scale = scale or None

    def setAndSaveScale(self, type_scale: TipoEscala, size: int, technique: Tecnica):
        self.scale = Escala.objects.create(
            id_tipo_escala=type_scale,
            longitud=size,
            tecnica=technique
        )

    def setScale(self, scale):
        self.scale = scale

    def realte_tags_type_cotinue(self, tags: list):
        tag = Etiqueta.objects.get(id=tags["punto_inicial"])
        start_point = EtiquetasEscala.objects.create(
            id_escala=self.scale.id,
            id_etiqueta=tag,
            posicion=1
        )

        tag = Etiqueta.objects.get(id=tags["punto_medio"])
        half_point = EtiquetasEscala.objects.create(
            id_escala=self.scale.id,
            id_etiqueta=tag,
            posicion=2
        )

        tag = Etiqueta.objects.get(id=tags["punto_final"])
        end_point = EtiquetasEscala.objects.create(
            id_escala=self.scale.id,
            id_etiqueta=tag,
            posicion=3
        )

        self.tags = [
            ("start", start_point),
            ("medium", half_point),
            ("end", end_point)
        ]

        return self.tags

    def realte_tags_type_structure(self, tags: dict):
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
            
        return self.tags
