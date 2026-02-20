from django.http import HttpRequest, JsonResponse
from utils import general_error
from tecnicas.controllers import RatingPFListController
import json


def apiListWordsPF(req:  HttpRequest):
    if req.method == "GET":
        return RatingPFListController.getListWords(request=req)
    elif req.method == "POST":
        try:
            data = json.loads(req.body.decode("utf-8"))
            phase = data.get("phase", [])
            if phase == 1 or phase == 2:
                raw_words = data.get("words", [])
                response = RatingPFListController.saveList(
                    request=req, current_phase=phase, words=raw_words)

            elif phase >= 3:
                word = data.get("word", [])
                raw_data = data.get("data", [])
                response = RatingPFListController.saveRatings(
                    request=req, word_rating=word, data=raw_data)

            return response
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "Error procesando datos"}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
