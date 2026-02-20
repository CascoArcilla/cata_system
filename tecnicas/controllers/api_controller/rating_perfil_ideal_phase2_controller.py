from django.db import transaction
from tecnicas.models import Calificacion, Escala, CalificacionEscala, DatoHedonico
from tecnicas.controllers import CalificacionController, DatoController
from utils import controller_error


class RatingPerfilIdealPhase2Controller():
    def __init__(self, rating_hedonic: Calificacion,
                 value_hedonic: int,
                 hedonic_scale: Escala):
        self.rating_hedonic = rating_hedonic
        self.value_hedonic = value_hedonic
        self.hedonic_scale = hedonic_scale

    def controllPostPhase2(self) -> dict:
        try:
            with transaction.atomic():
                # Obtener o crear calificación para escala hedónica con lock
                rating_hedonic = Calificacion.objects.select_for_update().get_or_create(
                    num_repeticion=self.rating_hedonic.num_repeticion,
                    id_producto=self.rating_hedonic.id_producto,
                    id_tecnica=self.rating_hedonic.id_tecnica,
                    id_catador=self.rating_hedonic.id_catador,
                    calificacion_escala__escala=self.hedonic_scale
                )[0]

                # Asociar calificación hedónica con su escala
                CalificacionEscala.objects.get_or_create(
                    calificacion=rating_hedonic,
                    escala=self.hedonic_scale
                )

                # Guardar dato hedónico
                data_hedonic = DatoHedonico.objects.create(
                    calificacion=rating_hedonic,
                    valor=self.value_hedonic
                )

                return {"message": "Calificación hedónica guardada exitosamente"}

        except Exception as e:
            return controller_error(f"Error al guardar la calificación hedónica: {str(e)}")
