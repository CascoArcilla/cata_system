from django.http import HttpRequest, JsonResponse
from tecnicas.utils import general_error
from tecnicas.controllers import RatingPFListController
import json


def apiListWordsPF(req:  HttpRequest):
    if req.method == "POST":
        try:
            data = json.loads(req.body.decode("utf-8"))
            raw_words = data.get("words", [])
            phase = data.get("phase", [])

            response = RatingPFListController.firstSaveList(
                request=req, current_phase=phase, words=raw_words)
            return response
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "Error procesando datos"}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
