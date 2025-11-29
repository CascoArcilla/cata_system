from django.http import HttpRequest, JsonResponse
from tecnicas.controllers import RatingNappingController
import json


def ratingNappingNoMode(req:  HttpRequest):
    if req.method == "POST":
        try:
            data = json.loads(req.body.decode("utf-8"))
            response = RatingNappingController.saveRatingCoordinates(
                request=req, data=data)
            return response
        except Exception as e:
            return JsonResponse({"error": "Error al procesar datos"})
    else:
        return JsonResponse({"error": "Método no permitido"})
