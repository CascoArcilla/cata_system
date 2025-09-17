from ..models import Calificacion, Tecnica


class CalificacionController():
    @staticmethod
    def getRatingsByTechnique(technique: Tecnica):
        repetition = technique.repecion

        if not repetition:
            return {"error": "sin datos calficados aun"}

        data_rating = {}

        for i in range(repetition):
            response_data = Calificacion.objects.filter(
                id_tecnica=technique, num_repeticion=i+1)
            data_rating[f"repeticion_{i+1}"] = response_data

        return data_rating
