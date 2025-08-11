from ..models import Escala, TipoEscala, Etiqueta, EtiquetasEscala

class BuildSensorySesion():

    def realte_tags(self, tags:list):
        if self.escala.id_tipo_escala.nombre_escala == "continua":
            tag = Etiqueta.objects.get(id=tags["punto_inicial"])
            start_point = EtiquetasEscala(id_escala = self.escala.id, id_etiqueta = tag, posicion = 1)

            tag = Etiqueta.objects.get(id=tags["punto_medio"])
            half_point = EtiquetasEscala(id_escala = self.escala.id, id_etiqueta = tag, posicion = 2)

            tag = Etiqueta.objects.get(id=tags["punto_final"])
            end_point = EtiquetasEscala(id_escala = self.escala.id, id_etiqueta = tag, posicion = 3)

        elif self.escala.id_tipo_escala.nombre_escala == "estructurda":
            tags.sort()