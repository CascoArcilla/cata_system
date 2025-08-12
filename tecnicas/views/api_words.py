from django.http import HttpRequest, JsonResponse
from django.db import IntegrityError
from ..models import Palabra


def words(req: HttpRequest):
    if req.method == "GET":
        try:
            word_name = req.GET["palabra"]
            fund_word = Palabra.objects.get(nombre_palabra=word_name)
        except KeyError:
            return error()
        except Palabra.DoesNotExist:
            return error("palabra no encontrada")

        response = {
            "message": "dato localizado",
            "data": {
                "id": fund_word.id,
                "name": fund_word.nombre_palabra,
            }
        }

        return JsonResponse(response)
    elif req.method == "POST":
        try:
            word_name = req.POST["nombre_palabra"]
            new_word = Palabra.objects.create(nombre_palabra=word_name)
        except KeyError:
            return error()
        except IntegrityError:
            return error("palabra repetida")

        response = {
            "message": "palabra creada",
            "data": new_word.to_dict()
        }

        return JsonResponse(response)


def error(message="parametros no encontrados"):
    respuesta = {"error": message}
    return JsonResponse(respuesta)
