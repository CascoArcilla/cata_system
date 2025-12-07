from django.http import HttpRequest, JsonResponse
from tecnicas.utils import general_error
from tecnicas.controllers import RatingCataController
import json


def ratingWordCata(req:  HttpRequest):
    if req.method == "POST":
        try:
            data = json.loads(req.body.decode("utf-8"))
            raw_words = data.get("words", [])
            raw_product = data.get("product", [])

            response = RatingCataController.saveRatingWords(
                request=req, data_words=raw_words, data_prodct=raw_product)
            return response
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "Error procesando datos"}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
