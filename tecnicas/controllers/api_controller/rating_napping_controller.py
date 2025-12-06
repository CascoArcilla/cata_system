from django.http import JsonResponse
from django.http import HttpRequest
from django.db import transaction
from tecnicas.models import Calificacion, DatoPunto, Producto, Participacion, Palabra
from tecnicas.forms import ListWordsForm


class RatingNappingController:
    @staticmethod
    def saveRatingCoordinates(request: HttpRequest, data: list):
        participation = Participacion.objects.get(
            id=request.session["id_participation"]
        )

        print(data)

        try:
            with transaction.atomic():
                products_map = RatingNappingController.getProductsMap(
                    participation.tecnica)

                existing_ratings_map = RatingNappingController.getExistingRatingsMap(
                    participation.tecnica, participation.catador
                )

                validation_result = RatingNappingController.validateWords(data)
                if validation_result is not None:
                    return validation_result

                new_ratings = []
                ids_products = products_map.keys()
                for item in data:
                    product_id = int(item["idProduct"])
                    if product_id not in existing_ratings_map and product_id in ids_products:
                        new_ratings.append(
                            Calificacion(
                                num_repeticion=0,
                                id_producto=products_map[product_id],
                                id_tecnica=participation.tecnica,
                                id_catador=participation.catador,
                            )
                        )

                if new_ratings:
                    Calificacion.objects.bulk_create(new_ratings)
                    existing_ratings_map = RatingNappingController.getExistingRatingsMap(
                        participation.tecnica, participation.catador
                    )

                existing_points_map = RatingNappingController.getExistingPointsMap(
                    existing_ratings_map.values())

                points_to_create = []
                points_to_update = []

                for item in data:
                    product_id = int(item["idProduct"])
                    rating = existing_ratings_map.get(product_id)

                    if rating:
                        if rating.id in existing_points_map:
                            point = existing_points_map[rating.id]
                            point.x = item["x"]
                            point.y = item["y"]
                            points_to_update.append(point)
                        else:
                            points_to_create.append(
                                DatoPunto(
                                    x=item["x"],
                                    y=item["y"],
                                    calificacion=rating,
                                )
                            )

                if points_to_create:
                    DatoPunto.objects.bulk_create(points_to_create)

                if points_to_update:
                    DatoPunto.objects.bulk_update(points_to_update, ['x', 'y'])

                RatingNappingController.processWordsForRatings(
                    data, existing_ratings_map
                )

            return JsonResponse({"message": "Datos guardados exitosamente"})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": "Error al procesar datos"})

    @staticmethod
    def validateWords(data: list):
        """Valida todas las palabras de todos los items usando ListWordsForm.
        Retorna JsonResponse con error si hay problemas, None si todo está bien."""
        for item in data:
            words = item.get("words", [])
            if words:
                dic_words = {}
                for index, word in enumerate(words, start=1):
                    dic_words[f"palabra_{index}"] = word

                form = ListWordsForm(dic_words, new_words=words)
                if not form.is_valid():
                    errors = []
                    for field, error_list in form.errors.items():
                        errors.extend(error_list)
                    return JsonResponse({"error": f"Error en validación de palabras: {', '.join(errors)}"})
        return None

    @staticmethod
    def processWordsForRatings(data: list, existing_ratings_map: dict):
        """Procesa y asocia palabras a las calificaciones.
        Crea palabras que no existan y las asocia a las calificaciones correspondientes."""

        all_words = set()
        for item in data:
            words = item.get("words", [])
            if words:
                all_words.update(words)

        if not all_words:
            return

        existing_words = Palabra.objects.filter(
            nombre_palabra__in=all_words
        )
        existing_words_map = {w.nombre_palabra: w for w in existing_words}

        word_objects = {}
        for word_name in all_words:
            if word_name in existing_words_map:
                word_objects[word_name] = existing_words_map[word_name]
            else:
                word_obj, created = Palabra.objects.get_or_create(
                    nombre_palabra=word_name
                )
                word_objects[word_name] = word_obj

        for item in data:
            words = item.get("words", [])
            if words:
                product_id = int(item["idProduct"])
                rating = existing_ratings_map.get(product_id)

                if rating:
                    words_to_set = [word_objects[word_name]
                                    for word_name in words]
                    rating.palabras.set(words_to_set)

    @staticmethod
    def getProductsMap(id_tecnica):
        products_qs = Producto.objects.filter(id_tecnica=id_tecnica)
        return {p.id: p for p in products_qs}

    @staticmethod
    def getExistingRatingsMap(id_tecnica, id_catador):
        ratings = Calificacion.objects.filter(
            id_tecnica=id_tecnica,
            id_catador=id_catador,
        )
        return {r.id_producto.id: r for r in ratings}

    @staticmethod
    def getExistingPointsMap(ratings):
        points = DatoPunto.objects.filter(calificacion__in=ratings)
        return {p.calificacion.id: p for p in points}
