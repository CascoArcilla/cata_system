from django.http import HttpRequest, JsonResponse


def reatingWord(req:  HttpRequest):
    if req.method == "POST":
        if not req.POST["rating-word"]:
            return JsonResponse({"error": "No se ha reconocido valor para la calificacion"})
        rating = req.POST["rating-word"]
        word = req.POST["name-word"]
        return JsonResponse({
            "message": "Ok",
            "data": {
                "word": word,
                "rating": rating,
                "cata_ser": req.session["cata_username"]
            }
        })
