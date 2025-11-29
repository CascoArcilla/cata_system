from django.http import JsonResponse
from django.http import HttpRequest
from django.db import transaction
from tecnicas.models import Calificacion, DatoPunto, Producto, Participacion


class RatingNappingController:
    @staticmethod
    def saveRatingCoordinates(request: HttpRequest, data: list):
        participation = Participacion.objects.get(
            id=request.session["id_participation"]
        )

        try:
            with transaction.atomic():
                products_map = RatingNappingController.getProductsMap(
                    participation.tecnica)

                existing_ratings_map = RatingNappingController.getExistingRatingsMap(
                    participation.tecnica, participation.catador
                )

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

            return JsonResponse({"message": "Datos guardados exitosamente"})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": "Error al procesar datos"})

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
