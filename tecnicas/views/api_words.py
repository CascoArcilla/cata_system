from django.http import HttpRequest, JsonResponse
from django.db import IntegrityError
from ..models import Palabra
from ..utils import general_error


def words(req: HttpRequest):
    if req.method == "GET":
        try:
            word_name = req.GET["palabra"]
            fund_words = Palabra.objects.filter(
                nombre_palabra__contains=word_name)
        except KeyError:
            return general_error("parametros no encontrados")
        
        if not fund_words:
            return general_error("no existen palabras")

        response_words = [word.to_dict() for word in fund_words]

        response = {
            "message": "datos localizados",
            "data": response_words
        }

        return JsonResponse(response)
    elif req.method == "POST":
        try:
            word_name = req.POST["nombre_palabra"]
            new_word = Palabra.objects.create(nombre_palabra=word_name)
        except KeyError:
            return general_error("parametros no encontrados")
        except IntegrityError:
            return general_error("palabra repetida")

        response = {
            "message": "palabra creada",
            "data": new_word.to_dict()
        }

        return JsonResponse(response)
