from django.http import JsonResponse, HttpRequest
from django.db import transaction
from tecnicas.models import Participacion, Palabra, GrupoProducto, Producto


class RatingSortController():
    def __init__(self):
        pass

    @staticmethod
    def saveRating(request: HttpRequest, data: list[dict]):
        try:
            with transaction.atomic():
                participation = Participacion.objects.get(
                    id=request.session["id_participation"])

                technique = participation.tecnica
                catador = participation.catador

                # Obtener productos de la técnica
                technique_products = Producto.objects.filter(
                    id_tecnica=technique)
                technique_product_ids = set(p.id for p in technique_products)

                # Recolectar IDs de productos enviados
                sent_product_ids = set()
                for group in data:
                    for product in group["products"]:
                        sent_product_ids.add(int(product["id"]))

                # Validar que los productos enviados existan en la técnica
                if not sent_product_ids.issubset(technique_product_ids):
                    return JsonResponse({"error": "Productos enviados no pertenecen a la técnica"})

                # Validar que todos los productos de la técnica estén presentes
                if sent_product_ids != technique_product_ids:
                    return JsonResponse({"error": "Faltan productos por clasificar"})

                for group in data:
                    words_data = group["words"]
                    products_data = group["products"]

                    # Crear u obtener palabras
                    words_objs = []
                    for word_name in words_data:
                        word, created = Palabra.objects.get_or_create(nombre_palabra=word_name)
                        words_objs.append(word)

                    # Crear GrupoProducto
                    group_product = GrupoProducto.objects.create(
                        tecnica=technique,
                        catador=catador
                    )

                    # Asignar palabras
                    group_product.palabras.set(words_objs)

                    # Asignar productos
                    product_ids = [p["id"] for p in products_data]
                    group_product.productos.set(product_ids)

            return JsonResponse({"message": "Valores guardados"})
        except Participacion.DoesNotExist:
            return JsonResponse({"error": "Participación no encontrada"})
        except Exception as e:
            print(f"Error de calificacion: {e}")
            return JsonResponse({"error": "Error al guardar los datos"})
