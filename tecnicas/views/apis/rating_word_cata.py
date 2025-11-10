from django.http import HttpRequest, JsonResponse
from tecnicas.utils import general_error
import json


def ratingWordCata(req:  HttpRequest):
    if req.method == "POST":
        try:
            data = json.loads(req.body.decode("utf-8"))
            words = data.get("words", [])

            print(words)

            return JsonResponse({"message": "Datos recibidos correctamente"})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "Error procesando datos"}, status=400)

    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
