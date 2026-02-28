from django.http import JsonResponse, HttpRequest
from django.db import transaction
from tecnicas.models import Calificacion, Dato, ValorBooleano, Participacion, Palabra


class RatingCataController():
    def __init__(self):
        pass

    @staticmethod
    def saveRatingWords(request: HttpRequest, data_words: list[dict], data_prodct: dict):
        try:
            with transaction.atomic():
                participation = Participacion.objects.get(
                    id=request.session["id_participation"])
                if not participation:
                    raise ValueError("No está autorizado en la sesión")

                ids_words = []
                words_values = {}

                # Acoplar datos para usar
                for da_wo in data_words:
                    ids_words.append(da_wo["id"])
                    words_values[da_wo["word"]] = da_wo["is_check"]

                words_for_rating = Palabra.objects.filter(id__in=ids_words)
                if not words_for_rating:
                    raise ValueError("No se han encontrado sus palabras")

                technique = participation.tecnica

                # Creando la calificacion
                (rating, creataed) = Calificacion.objects.get_or_create(
                    num_repeticion=technique.repeticion,
                    id_producto_id=data_prodct["id"],
                    id_tecnica=technique,
                    id_catador=request.user.user_catador
                )
                if not rating:
                    raise ValueError("Problemas al crear la calificación")

                # Guardando datos
                data_for_save = []
                for word in words_for_rating:
                    data_for_save.append(Dato(
                        id_palabra=word,
                        id_calificacion=rating
                    ))

                Dato.objects.bulk_create(data_for_save)
                data_saved = Dato.objects.filter(
                    id_calificacion=rating).only("id_palabra")
                if not data_saved:
                    raise ValueError("Problemas al crear los datos")

                # Guardando valores de datos
                values_for_save = []
                for data in data_saved:
                    word_for_rating = data.id_palabra.nombre_palabra
                    values_for_save.append(
                        ValorBooleano(
                            id_dato=data,
                            valor=words_values[word_for_rating]
                        )
                    )

                ValorBooleano.objects.bulk_create(values_for_save)
                values_saves = ValorBooleano.objects.filter(
                    id_dato__id_calificacion=rating).count()
                if not values_saves:
                    raise ValueError("Error al guardar los datos")

            return JsonResponse({"message": "Valores guardados"})

        except ValueError as e:
            print(f"Error de calificacion: {e}")
            return JsonResponse({"error": e}, statusstatus=500)
