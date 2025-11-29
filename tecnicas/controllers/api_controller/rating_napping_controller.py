from django.http import JsonResponse
from django.http import HttpRequest

class RatingNappingController:
    @staticmethod
    def saveRating(request: HttpRequest, data: list):
        print(data)

        try:
            return JsonResponse({"message": "Datos guardados exitosamente"})
        except Exception as e:
            return JsonResponse({"error": "Error al procesar datos"})
