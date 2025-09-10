from django.http import HttpRequest, JsonResponse
from django.db import IntegrityError
from ..models import Palabra
from ..utils import general_error
from ..forms.word_form import WordForm


def words(req: HttpRequest):
    if req.method == "GET":
        try:
            word_name = req.GET["palabra"]

            if word_name == "":
                fund_words = Palabra.objects.all()[:10]
            else:
                fund_words = Palabra.objects.filter(
                    nombre_palabra__startswith=word_name)
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
        form = WordForm(req.POST)

        if form.is_valid():
            form.cleaned_data["nombre_palabra"] = form.cleaned_data["nombre_palabra"].lower(
            )
            new_word = form.save()
            send_word = {
                "nombre_palabra": new_word.nombre_palabra,
                "id": new_word.id
            }
            response = {
                "message": "palabra creada",
                "data": send_word
            }
            return JsonResponse(response)
        else:
            errors = form.errors.get("nombre_palabra")
            return general_error(errors[0])
