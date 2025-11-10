from django.http import JsonResponse, HttpRequest
from django.db import transaction
from tecnicas.models import Calificacion, Dato, ValorBooleano, Participacion, Palabra


class RatingCataController():
    def __init__(self):
        pass

    @staticmethod
    def saveRatingWords(request: HttpRequest, data_words: list[dict]):
        try:
            with transaction.atomic():
                participation = Participacion.objects.get(
                    id=request.session["id_participation"])
                if not participation:
                    raise ValueError("No está autorizado en la sesión")
                
                # ids_words = [wo.id for ]
                
                words_for_rating = Palabra.objects.filter(id__in=ids_words)

                technique = participation.tecnica
                rating = Calificacion.objects.get_or_create(
                    num_repeticion=technique.repeticion
                    id_producto=1
                    id_tecnica=1
                    id_catador=1
                )
                pass
        except ValueError as e:
            print(f"Error de calificacion: {e}")
            return JsonResponse({"error": e}, statusstatus=500)
