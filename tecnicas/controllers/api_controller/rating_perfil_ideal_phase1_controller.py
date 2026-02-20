from django.db import transaction
from tecnicas.models import Calificacion, Escala, CalificacionEscala, ValorDecimal
from tecnicas.controllers import DatoController
from utils import controller_error


class RatingPerfilIdealPhase1Controller():
    def __init__(self, rating_intensity: Calificacion,
                 rating_ideal: Calificacion,
                 data_controller_intensity: DatoController,
                 data_controller_ideal: DatoController,
                 intensity_scale: Escala,
                 ideal_scale: Escala):
        self.rating_intensity = rating_intensity
        self.rating_ideal = rating_ideal
        self.data_controller_intensity = data_controller_intensity
        self.data_controller_ideal = data_controller_ideal
        self.intensity_scale = intensity_scale
        self.ideal_scale = ideal_scale

    def controllPostPhase1(self) -> dict:
        try:
            with transaction.atomic():
                # Obtener o crear calificación para escala de intensidad con lock
                save_rating_intensity = Calificacion.objects.select_for_update().get_or_create(
                    num_repeticion=self.rating_intensity.num_repeticion,
                    id_producto=self.rating_intensity.id_producto,
                    id_tecnica=self.rating_intensity.id_tecnica,
                    id_catador=self.rating_intensity.id_catador,
                    calificacion_escala__escala=self.intensity_scale
                )[0]

                # Asociar calificación de intensidad con su escala
                CalificacionEscala.objects.get_or_create(
                    calificacion=save_rating_intensity,
                    escala=self.intensity_scale
                )

                # Obtener o crear calificación para escala ideal con lock
                save_rating_ideal = Calificacion.objects.select_for_update().get_or_create(
                    num_repeticion=self.rating_ideal.num_repeticion,
                    id_producto=self.rating_ideal.id_producto,
                    id_tecnica=self.rating_ideal.id_tecnica,
                    id_catador=self.rating_ideal.id_catador,
                    calificacion_escala__escala=self.ideal_scale
                )[0]

                # Asociar calificación ideal con su escala
                CalificacionEscala.objects.get_or_create(
                    calificacion=save_rating_ideal,
                    escala=self.ideal_scale
                )

                # Guardar dato de intensidad
                self.data_controller_intensity.setRating(
                    new_rating=save_rating_intensity)
                data_intensity = self.data_controller_intensity.saveData()
                if isinstance(data_intensity, dict):
                    return controller_error(data_intensity["error"])

                value_intensity = ValorDecimal.objects.create(
                    valor=self.data_controller_intensity.value_rating,
                    id_dato=data_intensity
                )

                # Guardar dato ideal
                self.data_controller_ideal.setRating(
                    new_rating=save_rating_ideal)
                data_ideal = self.data_controller_ideal.saveData()
                if isinstance(data_ideal, dict):
                    return controller_error(data_ideal["error"])

                value_ideal = ValorDecimal.objects.create(
                    valor=self.data_controller_ideal.value_rating,
                    id_dato=data_ideal
                )

                return {"message": "Calificaciones guardadas exitosamente"}

        except Exception as e:
            print(e)
            return controller_error("Error al guardar las calificaciones")
